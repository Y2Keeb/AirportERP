# Luchthaven ERP
Ons project is een luchthaven ERP-systeem dat de operationele processen van een luchthaven digitaliseert en optimaliseert. 
Het biedt een centrale oplossing voor vluchtbeheer en passagiersafhandeling.
Veel luchthavens kampen met gefragmenteerde systemen en handmatige processen, wat leidt tot vertragingen, miscommunicatie en operationele fouten. 
Ons systeem centraliseert en stroomlijnt deze processen om de efficiëntie en veiligheid te verbeteren.
# Airport ERP 
Our project is an airport ERP system that digitizes and optimizes the operational processes of an airport. It provides a centralized solution for flight management and passenger handling. Many airports struggle with fragmented systems and manual processes, leading to delays, miscommunication, and operational errors. Our system centralizes and streamlines these processes to improve efficiency and safety.

# File structure
```
/airportERP
│── /src                 # Source code (main Python)
│── /docs                # Documentation (wireframes, planning,...)
│    ├── wireframes      # Wireframes
│── .gitignore           # Files to ignore in Git (like __pycache__,.idea,...)
│── README.md            # High-level project description
│── requirements.txt     # Non Built-in external dependencies
```
# Roles and Responsibilities
## Admin

- **Create users**
- **Manage roles**
  - *Add roles*
  - *Remove roles*

## Flight Planner

- **Plan flights**

## Security Border

- **Flag names** (e.g., Bjorn Wijn → Red) (Naam ingeven → Rood)

## Bagage Claim
- Status bagage + location 
- Paired to flight_id and passager_id

## Manager (operationeel plannen)

- *Show flights
- *Adjust salary of employees
- *Beheer afwezigheden*


## Maintenance (Onderhoud)

- **Maintain warehouse database**

## ATC Tower (ATC Toren)

*(Responsibilities not specified)*

## Cafeteria (Cafetaria)

- **Add extra lounge**

## User (Gebruiker)

- **Buy tickets** (Ticket kopen)
- **Earn points** (Puntensparen)
- **Check flight details** (Vlucht raadplegen)
- **Upgrade class** (Klasse verhogen)
- **Access lounge** (Lounge toegang)
- **Use QR code tickets** (QR-code ticket)

## Airline (Vliegtuigmaatschappij)

- **Offer flights** (Vluchten aanbieden)



# TO DO 
1. Admin page (Thomas)
1. Login scherm (Thomas)
1. Database opzetten en DBConnector (Reza) 
2. Database Tables (Lindsey)
2. Flight Planner vormgeven (Lindsey)
2. Flight Planner functies
3. User Page vormgeven met data van flight


# Technical
- Database: **mySQL**
- UI: **Tkinter**
- External Packages: **Pillow** (image processing for airline logos) 

