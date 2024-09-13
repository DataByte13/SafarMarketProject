using ApplicationWebApi.Dtos;
using ApplicationWebApi.Models;

namespace ApplicationWebApi.Interfaces
{
    public interface ITravelLocations
    {
        List<GetTravelLocatoinDto> GetLocatoins(LatitudeAndLongitude Geographiccoordinates, int radiusKm);
        bool SetRateOnLocatoin(int Id, float newRate);

    }
}
