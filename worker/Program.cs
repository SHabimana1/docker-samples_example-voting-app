using System;
using System.Data.Common;
using System.Diagnostics;
using System.Linq;
using System.Net;
using System.Net.Sockets;
using System.Threading;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Hosting;
using Newtonsoft.Json;
using Npgsql;
using Serilog;
using Serilog.Formatting.Json;
using StackExchange.Redis;
using OpenTelemetry;
using OpenTelemetry.Trace;
using OpenTelemetry.Resources;

namespace Worker
{
    public class Program
    {
        public static int Main(string[] args)
        {
            // ---- Serilog setup ----
            Log.Logger = new LoggerConfiguration()
                .WriteTo.Console(new JsonFormatter())
                .CreateLogger();

            try
            {
                // ---- Host + DI + OpenTelemetry ----
                using var host = Host.CreateDefaultBuilder(args)
                    .ConfigureServices(services =>
                    {
                        services.AddOpenTelemetry()
                            .WithTracing(builder => builder
                                .AddSource("Worker")
                                .SetResourceBuilder(
                                    ResourceBuilder.CreateDefault()
                                        .AddService("Worker")
                                )
                                .AddOtlpExporter(opt =>
                                {
                                    opt.Endpoint = new Uri("https://<your-env>.live.dynatrace.com/api/v2/otlp");
                                    opt.Headers = "Authorization=Api-Token <token>";
                                })
                            );
                    })
                    .Build();

                var tracerProvider = host.Services.GetRequiredService<TracerProvider>();
                var tracer = tracerProvider.GetTracer("Worker");

                // ---- Worker infrastructure ----
                var pgsql = OpenDbConnection("Server=db;Username=postgres;Password=postgres;");
                var redisConn = OpenRedisConnection("redis");
                var redis = redisConn.GetDatabase();

                var keepAliveCommand = pgsql.CreateCommand();
                keepAliveCommand.CommandText = "SELECT 1";

                var definition = new { vote = "", voter_id = "", traceparent = "" };

                // ---- Main worker loop ----
                while (true)
                {
                    Thread.Sleep(100);

                    if (redisConn == null || !redisConn.IsConnected)
                    {
                        Console.WriteLine("Reconnecting Redis");
                        redisConn = OpenRedisConnection("redis");
                        redis = redisConn.GetDatabase();
                    }

                    string json = redis.ListLeftPopAsync("votes").Result;
                    if (json != null)
                    {
                        var vote = JsonConvert.DeserializeAnonymousType(json, definition);

                        // ---- Extract parent trace context ----
                        ActivityContext parentContext = default;
                        bool hasParent = false;

                        if (!string.IsNullOrEmpty(vote.traceparent))
                        {
                            parentContext = ActivityContext.Parse(vote.traceparent, null);
                            hasParent = true;
                        }

                        // ---- Create Worker Activity with correct parent ----
                        using (var activity = hasParent
                            ? tracer.StartActivity(
                                "Worker.ProcessVote",
                                ActivityKind.Consumer,
                                parentContext)
                            : tracer.StartActivity("Worker.ProcessVote", ActivityKind.Consumer))
                        {
                            // Add logging fields
                            Log.ForContext("traceId", activity?.TraceId.ToString())
                               .ForContext("spanId", activity?.SpanId.ToString())
                               .Information("Processing vote for {VoteChoice} by {VoterId}",
                                    vote.vote, vote.voter_id);

                            // ---- DB Logic ----
                            if (!pgsql.State.Equals(System.Data.ConnectionState.Open))
                            {
                                Console.WriteLine("Reconnecting DB");
                                pgsql = OpenDbConnection("Server=db;Username=postgres;Password=postgres;");
                            }
                            else
                            {
                                UpdateVote(pgsql, vote.voter_id, vote.vote);
                            }
                        }
                    }
                    else
                    {
                        keepAliveCommand.ExecuteNonQuery();
                    }
                }
            }
            catch (Exception ex)
            {
                Console.Error.WriteLine(ex.ToString());
                return 1;
            }
        }

        // ----------------------------------------
        // Helpers
        // ----------------------------------------

        private static NpgsqlConnection OpenDbConnection(string connectionString)
        {
            NpgsqlConnection connection;
            while (true)
            {
                try
                {
                    connection = new NpgsqlConnection(connectionString);
                    connection.Open();
                    break;
                }
                catch (Exception)
                {
                    Console.Error.WriteLine("Waiting for db");
                    Thread.Sleep(1000);
                }
            }
            Console.Error.WriteLine("Connected to db");

            var command = connection.CreateCommand();
            command.CommandText = @"CREATE TABLE IF NOT EXISTS votes (
                                        id VARCHAR(255) NOT NULL UNIQUE,
                                        vote VARCHAR(255) NOT NULL
                                    )";
            command.ExecuteNonQuery();
            return connection;
        }

        private static ConnectionMultiplexer OpenRedisConnection(string hostname)
        {
            var ipAddress = GetIp(hostname);
            Console.WriteLine($"Found redis at {ipAddress}");
            while (true)
            {
                try
                {
                    Console.Error.WriteLine("Connecting to redis");
                    return ConnectionMultiplexer.Connect(ipAddress);
                }
                catch (RedisConnectionException)
                {
                    Console.Error.WriteLine("Waiting for redis");
                    Thread.Sleep(1000);
                }
            }
        }

        private static string GetIp(string hostname)
            => Dns.GetHostEntryAsync(hostname)
                .Result
                .AddressList
                .First(a => a.AddressFamily == AddressFamily.InterNetwork)
                .ToString();

        private static void UpdateVote(NpgsqlConnection connection, string voterId, string vote)
        {
            var command = connection.CreateCommand();
            try
            {
                command.CommandText = "INSERT INTO votes (id, vote) VALUES (@id, @vote)";
                command.Parameters.AddWithValue("@id", voterId);
                command.Parameters.AddWithValue("@vote", vote);
                command.ExecuteNonQuery();
            }
            catch (DbException)
            {
                command.CommandText = "UPDATE votes SET vote = @vote WHERE id = @id";
                command.ExecuteNonQuery();
            }
            finally
            {
                command.Dispose();
            }
        }
    }
}
