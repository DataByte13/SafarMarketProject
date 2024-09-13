using ApplicationWebApi.Dtos;
using ApplicationWebApi.Interfaces;
using ApplicationWebApi.Models;
using System;
using System.Linq;
namespace ApplicationWebApi.Features
{
    public class TravelLocations : ITravelLocations
    {
        private const double EarthRadiusKm = 6371.0; // Radius of the Earth in kilometers
        private readonly LocationsDataBaseContext _context;

        public TravelLocations(LocationsDataBaseContext context)
        {
            _context = context;
        }

        public List<GetTravelLocatoinDto> GetLocatoins(LatitudeAndLongitude geographicCoordinates, int radiusKm)
        {
            // Fetch all locations from the database
            // Fetch all relevant locations from the database
            var locations = _context.Locations
                .AsEnumerable() // Convert to IEnumerable to perform in-memory operations
                .Select(location => new
                {
                    Id = location.Id,
                    Latitude = location.Latitude,
                    Longitude = location.Longitude
                })
                .ToList(); // Fetch all data first

            // Filter locations based on distance calculation
            var result = new List<GetTravelLocatoinDto>();

            foreach (var location in locations)
            {
                var distance = GetDistanceInKm(
                    geographicCoordinates.Latitude,
                    geographicCoordinates.Longitude,
                    (float)location.Latitude.GetValueOrDefault(),
                    (float)location.Longitude.GetValueOrDefault());

                if (distance <= radiusKm)
                {
                    var acceptedLocation = _context.Locations
                        .FirstOrDefault(l => l.Id == location.Id);
                    result.Add(new GetTravelLocatoinDto
                    {
                        Id = acceptedLocation.Id,
                        Name = acceptedLocation.Title,
                        Description = acceptedLocation.Description,
                        Type = acceptedLocation.Type ?? default(string),
                        Rate = (float)acceptedLocation.Rate.GetValueOrDefault(),
                        Ratecount = acceptedLocation.RateCount.GetValueOrDefault()
                    });
                }
            }


            return result;
        }

        private double GetDistanceInKm(float lat1, float lon1, float lat2, float lon2)
        {
            // Convert latitude and longitude from degrees to radians
            double lat1Rad = DegreesToRadians(lat1);
            double lon1Rad = DegreesToRadians(lon1);
            double lat2Rad = DegreesToRadians(lat2);
            double lon2Rad = DegreesToRadians(lon2);

            // Haversine formula
            double dlat = lat2Rad - lat1Rad;
            double dlon = lon2Rad - lon1Rad;

            double a = Math.Sin(dlat / 2) * Math.Sin(dlat / 2) +
                       Math.Cos(lat1Rad) * Math.Cos(lat2Rad) *
                       Math.Sin(dlon / 2) * Math.Sin(dlon / 2);

            double c = 2 * Math.Atan2(Math.Sqrt(a), Math.Sqrt(1 - a));
            double distance = EarthRadiusKm * c;

            return distance;
        }

        private double DegreesToRadians(double degrees)
        {
            return degrees * (Math.PI / 180.0);
        }


        public bool SetRateOnLocatoin(int Id, float newRate)
        {
            var location = _context.Locations.FirstOrDefault(l => l.Id == Id);
            if (location == null)
            {
                return false;
            }
            if (location.RateCount == 0)
            {
                location.Rate = newRate;
            }
            else
            {
                location.Rate = (location.Rate * location.RateCount + newRate) / (location.RateCount + 1);
            }
            location.RateCount += 1;
            _context.SaveChanges();
            return true;
        }
    }
}

