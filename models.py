from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, func
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.orm import sessionmaker

db_url = "sqlite:///concerts.db"
engine = create_engine(db_url)

Base = declarative_base()

#create bands table
class Band(Base):
    __tablename__ = "bands"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    hometown = Column(String)

    #band has many concerts(one to many)
    concerts = relationship("Concert", back_populates="band")
    #band has many to many relationship with venue
    venues = relationship("Venue", secondary="concerts", back_populates="bands", overlaps="concerts")

    #play_in_venue() method: takes a venue (Venue instance) and date (as a string) as arguments 
    # creates a new concert for the band in that venue on that date\
    def play_in_venue(self, venue, date, session):
        new_concert = Concert(date=date, band=self, venue=venue)
        session.add(new_concert)
        session.commit()#adds new concert to db
        return new_concert

    # all_introductions()Method to return all introductions for the band's concerts
    def all_introductions(self):
        introductions = []# will contain intros for concerts by the band
        for concert in self.concerts:#loops through all concerts for that band
            intro = f"Hello {concert.venue.city}!!!!! We are {self.name} and we're from {self.hometown}"
            introductions.append(intro)
        return introductions

    # Class method to find the band with the most performances
    @classmethod
    def most_performances(cls, session):
        all_bands = session.query(cls).all()  # Get all bands
        band_with_most_concerts = None
        most_concerts = 0

        # Loop through each band and count their concerts
        for band in all_bands:
            num_concerts = len(band.concerts)  # Count the concerts for this band
            if num_concerts > most_concerts:
                most_concerts = num_concerts
                band_with_most_concerts = band

        return band_with_most_concerts  # Return the band with the most concerts

#create venues table
class Venue(Base):
    __tablename__ = "venues"

    id = Column(Integer, primary_key=True)
    title = Column(String)
    city = Column(String)

    #venue has many concerts(one to many)
    concerts = relationship("Concert", back_populates="venue")
    #venue has many to many relationship with band 
    bands = relationship("Band", secondary="concerts", back_populates="venues", overlaps="concerts")

    #def concert_on(date):returns the first concert on the given date at this venue
    def concert_on(self, session, date):
        #returns the first concert on the given date at this venue
        # Query for the first concert at this venue on the given date
        concert = session.query(Concert).filter_by(venue_id=self.id, date=date).first()
        
        return concert

    #Most_frequent_band(): returns band with most concertas at a given venue
    def Most_frequent_band(self, session):
        # Join Band and Concert, group by band, and count the concerts
        most_frequent_band = (
            session.query(Band)
            .join(Concert)
            .filter(Concert.venue_id == self.id)
            .group_by(Band.id)
            .order_by(func.count(Concert.id).desc())
            .first()
        )
        return most_frequent_band
            
        


    
#create concert table
class Concert(Base):
    __tablename__="concerts"
    id = Column(Integer, primary_key=True)
    date = Column(String)
    #foreign keys
    band_id = Column(Integer, ForeignKey("bands.id"))#foreign key to band table
    venue_id = Column(Integer, ForeignKey("venues.id"))#foreign key to venue table
    #relationships
    band = relationship("Band", back_populates="concerts", overlaps="venues, bands")#a concert belongs to a band
    venue = relationship("Venue", back_populates="concerts", overlaps="bands, venues")#a concert belongs to a band

    #hometown_show() method for checking if hometown matches venue city
    def hometown_show(self):
        return self.venue.city == self.band.hometown # check if hometown matches venue city

    #introduction() method
    def introduction(self):
        return f"Hello {self.venue.city}!!!!! We are {self.band.name} and we're from {self.band.hometown}"

#creates tables to db
Base.metadata.create_all(engine)