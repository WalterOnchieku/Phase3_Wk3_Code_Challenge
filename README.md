# WK3 CODE CHALLENGE - CONCERTS

## Overview
The goal of this project is to build a **Concert Management Domain** using **Python 3** and **SQLAlchemy**. This challenge will test the following topics:
- SQLAlchemy Migrations
- SQLAlchemy Relationships
- Class and Instance Methods
- SQLAlchemy Querying

## Project Structure
The main files for this project are:
- `models.py`
- `app.py`

### 1. `models.py`
This file contains the models responsible for creating the tables in the database. There are three models:

- **Band**: `name`, `hometown`
- **Venue**: `title`, `city`
- **Concert**

The **Concert** table serves as an association table and contains two foreign keys: one matching the `Band` table's `id`, and the other matching the `Venue` table's `id`.

### Relationships
The following relationships between the tables have been defined:
- A Band has many Concerts.
- A Venue has many Concerts.
- A Concert belongs to both a Band and a Venue.
- The relationship between Band and Venue is many-to-many.

### Methods
Each model (class) has the following methods defined:

#### Object Relationship Methods
**Concert**
- `band()`: Returns the Band instance for this Concert.
- `venue()`: Returns the Venue instance for this Concert.
  
(Note: The above methods were implemented directly from the relationships and do not need to be defined separately as they would be redundant.)

**Venue**
- `concerts()`: Returns a collection of all the concerts for the Venue.
- `bands()`: Returns a collection of all the bands who performed at the Venue.

**Band**
- `concerts()`: Returns a collection of all the concerts that the Band has played.
- `venues()`: Returns a collection of all the venues where the Band has performed.

#### Aggregate and Relationship Methods
**Concert**
- `hometown_show()`: Returns `True` if the concert is in the band's hometown, otherwise `False`.
- `introduction()`: Returns a string in the form:  
  `"Hello {venue city}!!!!! We are {band name} and we're from {band hometown}"`.

**Band**
- `play_in_venue(venue, date)`: Takes a `Venue` instance and `date` (as a string) and creates a new concert for the band at that venue on that date.
- `all_introductions()`: Returns an array of strings representing all the introductions for this band in the form:  
  `"Hello {venue city}!!!!! We are {band name} and we're from {band hometown}"`.
- `most_performances()` (class method): Returns the Band instance that has played the most concerts.

**Venue**
- `concert_on(date)`: Takes a `date` (string) and returns the first concert on that date at the venue.
- `most_frequent_band()`: Returns the band with the most concerts at the venue.

### 2. `app.py`
This file contains:
- Instances of Band, Venue, and Concert to populate the corresponding tables.
- Implementations of all the methods defined in `models.py`.
- Additional queries to manage and manipulate the concert data.

## Installation
Clone the repository:
    ```bash
    git clone <https://github.com/WalterOnchieku/Phase3_Wk3_Code_Challenge>
    ```


## Usage
Once cloned, type code . to open in VS code
To run the application, execute:
```bash
python app.py
NB: ensure you are in the project root directory
