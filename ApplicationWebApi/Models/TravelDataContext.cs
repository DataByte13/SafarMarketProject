using System;
using System.Collections.Generic;
using Microsoft.EntityFrameworkCore;

namespace ApplicationWebApi.Models;

public partial class TravelDataContext : DbContext
{
    public TravelDataContext()
    {
    }

    public TravelDataContext(DbContextOptions<TravelDataContext> options)
        : base(options)
    {
    }

    public virtual DbSet<Location> Locations { get; set; }


    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
        modelBuilder
            .UseCollation("utf8mb4_unicode_ci")
            .HasCharSet("utf8mb4");

        modelBuilder.Entity<Location>(entity =>
        {
            entity.HasKey(e => e.Id).HasName("PRIMARY");

            entity.ToTable("locations");

            entity.Property(e => e.Id)
                .HasColumnType("int(11)")
                .HasColumnName("id");
            entity.Property(e => e.Description).HasColumnType("text");
            entity.Property(e => e.Image).HasMaxLength(255);
            entity.Property(e => e.RateCount).HasColumnType("int(11)");
            entity.Property(e => e.SafarMarketId)
                .HasMaxLength(255)
                .HasColumnName("SafarMarketID");
            entity.Property(e => e.Slug).HasMaxLength(255);
            entity.Property(e => e.Title).HasMaxLength(255);
            entity.Property(e => e.Type).HasMaxLength(255);
        });

        OnModelCreatingPartial(modelBuilder);
    }

    partial void OnModelCreatingPartial(ModelBuilder modelBuilder);
}
