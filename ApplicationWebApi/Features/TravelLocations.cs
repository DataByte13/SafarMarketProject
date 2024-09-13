using ApplicationWebApi.Dtos;
using ApplicationWebApi.Interfaces;
using ApplicationWebApi.Models;
namespace ApplicationWebApi.Features
{
    public class TravelLocations : ITravelLocations
    {
        private readonly TravelDataContext _context;
        static TravelLocations(TravelDataContext context)
        {
            _context = context;
        }

        public GetTravelLocatoinDto GetLocatoins(LatitudeAndLongitude Origin, LatitudeAndLongitude destination)
        {
            
        }

        public bool SetRateOnLocatoin(int Id, float rate)
        {
            
        }
    }
}

