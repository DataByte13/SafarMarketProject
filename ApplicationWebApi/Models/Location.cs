using System;
using System.Collections.Generic;

namespace ApplicationWebApi.Models;

public partial class Location
{
    public int Id { get; set; }

    public int? SafarMarketId { get; set; }

    public string? Title { get; set; }

    public string? Description { get; set; }

    public float? Latitude { get; set; }

    public float? Longitude { get; set; }

    public string? Type { get; set; }

    public string? Image { get; set; }

    public string? Slug { get; set; }

    public float? Rate { get; set; }

    public int? RateCount { get; set; }
}
