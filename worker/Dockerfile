# TAHAP 1: BUILD
FROM mcr.microsoft.com/dotnet/sdk:6.0 AS build
WORKDIR /app
COPY *.csproj .
RUN dotnet restore

COPY . .
RUN dotnet publish -c release -o /out

# TAHAP 2: FINAL
FROM mcr.microsoft.com/dotnet/runtime:6.0
WORKDIR /app
COPY --from=build /out .
ENTRYPOINT ["dotnet", "Worker.dll"]