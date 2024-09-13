using ApplicationWebApi.Features;
using ApplicationWebApi.Interfaces;
using Microsoft.EntityFrameworkCore;
using ApplicationWebApi.Models;


var builder = WebApplication.CreateBuilder(args);

// Add services to the container.

builder.Services.AddControllers();
// Learn more about configuring Swagger/OpenAPI at https://aka.ms/aspnetcore/swashbuckle
builder.Services.AddEndpointsApiExplorer();
builder.Services.AddSwaggerGen();
// dbcontex and stuff
var configuring = builder.Configuration;

var connectionString = Environment.GetEnvironmentVariable("TravelConnectionString") ??
builder.Configuration.GetConnectionString("TravelConnectionString");

builder.Services.AddDbContext<LocationsDataBaseContext>(options =>
    options.UseMySql(connectionString, new MySqlServerVersion(new Version(8, 0, 32))
      ));
builder.Services.AddScoped<DbContext, LocationsDataBaseContext>();
//--------------DI
builder.Services.AddScoped<ITravelLocations, TravelLocations>();


var app = builder.Build();

// Configure the HTTP request pipeline.
if (app.Environment.IsDevelopment())
{
    app.UseSwagger();
    app.UseSwaggerUI();
}

app.UseHttpsRedirection();

app.UseAuthorization();

app.MapControllers();

app.Run();
