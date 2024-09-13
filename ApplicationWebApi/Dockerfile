FROM mcr.microsoft.com/dotnet/sdk:7.0 AS build

WORKDIR /app

COPY *.csproj ./

RUN dotnet add package Microsoft.EntityFrameworkCore.Design --version 7.0.20 \
    && dotnet add package Microsoft.Extensions.DependencyInjection \
    && dotnet add package Pomelo.EntityFrameworkCore.MySql --version 7.0.0

RUN dotnet restore

COPY . ./

RUN dotnet publish -c Release -o out

FROM mcr.microsoft.com/dotnet/aspnet:7.0 AS runtime
WORKDIR /app

COPY --from=build /app/out .

EXPOSE 80

ENTRYPOINT ["dotnet", "ApplicationWebApi.dll"]
