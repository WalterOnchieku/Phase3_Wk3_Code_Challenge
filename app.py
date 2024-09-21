from sqlalchemy.orm import sessionmaker
from models import Band, Venue, Concert, engine, Base

#create session class
Session = sessionmaker(bind=engine)
#create session
session = Session()

#band instances
band1 = Band(name="Sauti Sol", hometown="Kakamega")
band2 = Band(name="Elani", hometown="Nairobi")
band3 = Band(name="Jabali", hometown="Mombasa")

#venue instances
venue1 = Venue(title="Safari Park Hotel", city="Nairobi")
venue2 = Venue(title="Sarova Whitesands Beach Resort", city="Mombasa")
venue3 = Venue(title="Leisure Lodge Hotel", city="Diani")

#concert instances
concert1 = Concert(date="2024/09/11", band=band2, venue=venue1)
concert2 = Concert(date="2024/12/08", band=band3, venue=venue2)
concert3 = Concert(date="2024/10/15", band=band1, venue=venue3)
concert4 = Concert(date="2024/09/19", band=band2, venue=venue3)
concert5 = Concert(date="2024/11/15", band=band3, venue=venue2)
concert6 = Concert(date="2024/10/12", band=band1, venue=venue1)

#add all instances to session
session.add_all([band1, band2, band3, venue1, venue2, venue3, concert1, concert2, concert3, concert4, concert5, concert6])
#commit transaction to save to database
session.commit()

concerts = session.query(Concert).all()
for concert in concerts:
    print(f"Band: {concert.band.name} | Venue: {concert.venue.title} | Date: {concert.date}")


# Object Relationship Methods

# Concerts
# Concert band():should return the Band instance for this Concert
concert = session.query(Concert).first()#query the first concert
band_instance_for_concert = concert.band #get band instance for first concert 
print(f"Band name: {band_instance_for_concert.name}, Hometown: {band_instance_for_concert.hometown}")

#Concert venue():should return the venue instance for this Concert
concert = session.query(Concert).first()#query the first concert
venue_instance_for_concert = concert.venue #get venue instance for first concert 
print(f"Venue title: {venue_instance_for_concert.title}, City: {venue_instance_for_concert.city}")

#Venues
#Venue concerts(): returns a collection of all the concerts for the Venue
venue = session.query(Venue).filter_by(title = "Sarova Whitesands Beach Resort").first()
venue_concerts = venue.concerts #get concerts for venue
print(f"concerts at {venue.title} in {venue.city}")#prints concert venue
for concert in venue_concerts:
    print(f"Concert Date: {concert.date}, Band: {concert.band.name}")#prints concerts in the concert table for the given venue

#Venue bands(): returns a collection of all the bands performing at the Venue
venue = session.query(Venue).filter_by(title = "Sarova Whitesands Beach Resort").first()
venue_bands = venue.bands 
print(f"bands at {venue.title} in {venue.city}")
for band in venue_bands:
    print(f"Band Name: {band.name}, Hometown: {band.hometown}")

#Bands
#band concerts():should return a collection of all the concerts that the Band has played
band = session.query(Band).first()#query the first band
band_concerts = band.concerts # get all concerts the band has played
print(f"Concerts played by {band.name}:")
for concert in band_concerts:
    print(f"Concert Date: {concert.date}, Venue: {concert.venue.title}")

#band venues():should return a collection of all the venues that the Band has performed at
band = session.query(Band).first()#query the first band
band_venues = band.venues # get all concerts the band has played
print(f"Venues played by {band.name}:")
for venue in band_venues:
    print(f"Venue: {venue.title}, City: {venue.city}")


#Aggregate and Relationship Methods

# concert
# Concert hometown_show(): returns true if the concert is in the band's hometown, false if it is not
concert = session.query(Concert).first() # Get the first concert
print(f"Band: {concert.band.name}, Hometown: {concert.band.hometown}")
print(f"Venue: {concert.venue.title}, City: {concert.venue.city}")
if concert.hometown_show():
    print(True)
else:
    print(False)

#Concert introduction(): returns a string with the band's introduction for this concert
concert = session.query(Concert).filter_by(date="2024/09/19").first()  # Get the concert, filter by date
print(concert.introduction())

# band
# Band play_in_venue(venue, date):takes a venue (Venue instance) and date (as a string) as arguments
# creates a new concert for the band in that venue on that date
band = session.query(Band).filter_by(name="Elani").first()  # Get the band "Elani"
venue = session.query(Venue).filter_by(title="Safari Park Hotel").first()  # Get the venue "Safari Park Hotel"
new_concert = band.play_in_venue(venue, "2024-10-30", session)# choose date for band to play
# Print the details of the new concert
print(f"New concert on {new_concert.date} at {new_concert.venue.title} by {new_concert.band.name}")

# all_introductions()Method:returns all introductions for the band's concerts
#Get a band
band = session.query(Band).filter_by(name="Elani").first()  # Get the band "Elani"
introductions = band.all_introductions()# Get all introductions for this band

# Print each introduction
for intro in introductions:
    print(intro)


# Band most_performances() class method:returns the Band instance for the band that has played the most concerts
# Find the band with the most performances
band_with_most_concerts = Band.most_performances(session)
print(f"The band with the most performances is {band_with_most_concerts.name}.")

#def concert_on(date):returns the first concert on the given date at this venue
venue = session.query(Venue).filter_by(title="Sarova Whitesands Beach Resort").first()
concert = venue.concert_on(session, "2024/12/08")

if concert:
    print(f"{concert.band.name} band performing at {concert.venue.title} on {concert.date}")
else:
    print("No concert found on that date.")

#Most_frequent_band(): returns band with most concertas at a given venue
venue = session.query(Venue).filter_by(title="Sarova Whitesands Beach Resort").first()
most_frequent_band = venue.most_frequent_band(session)

if most_frequent_band:
    print(f"The band that performed the most at {venue.title} is {most_frequent_band.name}.")
else:
    print(f"No band has performed at {venue.title}.")


