using ApplicationWebApi.Dtos;
using ApplicationWebApi.Models;

namespace ApplicationWebApi.Interfaces
{
    public interface ITravelLocations
    {
        GetTravelLocatoinDto GetLocatoins(LatitudeAndLongitude Origin, LatitudeAndLongitude destination);
        bool SetRateOnLocatoin(int Id ,float rate);
      
    }
}
