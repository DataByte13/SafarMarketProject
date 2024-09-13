using ApplicationWebApi.Dtos;
using ApplicationWebApi.Interfaces;
using ApplicationWebApi.Models;
using Microsoft.AspNetCore.Mvc;

namespace ApplicationWebApi.Controllers;
[ApiController]
[Route("[controller]")]
public class LocationController:Controller 
{
    private ITravelLocations _travelLocations;

    public LocationController(ITravelLocations travelLocations)
    {
        _travelLocations = travelLocations;
    }

    [HttpPost("GetLocations")]
    public async Task<ActionResult<List<GetTravelLocatoinDto>>> GetLocations(float Latitude , float Longitude  ,int radiusKm = 10 )
    {
        var geographiccoordinates = new LatitudeAndLongitude()
        {
            Latitude =Latitude,
            Longitude = Longitude
        };
        List<GetTravelLocatoinDto> locatoins = _travelLocations.GetLocatoins(geographiccoordinates, radiusKm);
        if (locatoins.Count == 0)
        {
            return Ok(new List<GetTravelLocatoinDto>());
        }

        return Ok(locatoins);
    }

    [HttpGet("rating")]
    public async Task<ActionResult> Rating(int Id, float rate)
    {
        if (_travelLocations.SetRateOnLocatoin(Id, rate))
        {
            return Ok();
        }
        return StatusCode(StatusCodes.Status500InternalServerError, "The rating was not recorded. Try again");
    }
}