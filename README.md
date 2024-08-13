# Flight Management System

## Overview

The Flight Management System is a Django-based application designed to handle various aspects of airline operations,
including managing airports, routes, airplanes, crews, flights, orders, and tickets. The system provides functionalities
for creating and managing these entities, as well as RESTful APIs for interacting with them.

## Features

- **Airport Management**: Add and manage airports and their closest big cities.
- **Route Management**: Define routes between airports, ensuring unique routes with specific distances.
- **Airplane Management**: Register different types of airplanes, including their capacities and images.
- **Crew Management**: Manage crew members, including their names and assignments.
- **Flight Management**: Schedule and manage flights, linking them with routes, airplanes, and crew members.
- **Order and Ticket Management**: Create orders and manage tickets, ensuring seat availability and consistency.

## Models

### Airport

- **name**: Name of the airport.
- **closest_big_city**: The nearest major city to the airport.

### Route

- **distance**: Distance of the route.
- **source**: Source airport (ForeignKey).
- **destination**: Destination airport (ForeignKey).

### AirplaneType

- **name**: Type of the airplane (e.g., Boeing 747).

### Airplane

- **name**: Name of the airplane.
- **rows**: Number of rows in the airplane.
- **seats_in_row**: Number of seats per row.
- **airplane_type**: Type of the airplane (ForeignKey).
- **image**: Image of the airplane.

### Crew

- **first_name**: First name of the crew member.
- **last_name**: Last name of the crew member.

### Flight

- **departure_time**: Departure time of the flight.
- **arrival_time**: Arrival time of the flight.
- **route**: Route of the flight (ForeignKey).
- **airplane**: Airplane used for the flight (ForeignKey).
- **crew**: Crew members assigned to the flight (ManyToManyField).

### Order

- **created_at**: Timestamp of when the order was created.
- **user**: User who created the order (ForeignKey).

### Ticket

- **row**: Row number in the airplane.
- **seat**: Seat number in the airplane.
- **flight**: Flight associated with the ticket (ForeignKey).
- **order**: Order associated with the ticket (ForeignKey).

## Summary

The Flight Management System provides a comprehensive solution for managing various aspects of airline operations
through its Django-based framework. By offering robust functionalities for managing airports, routes, airplanes, crews,
flights, orders, and tickets, the system ensures efficient and effective handling of airline data. With its RESTful
APIs, users can interact with and manage these entities programmatically, making it an essential tool for modern airline
management. Whether you're scheduling flights, managing crews, or handling ticket orders, this system streamlines and
simplifies the process, ensuring a smooth operational workflow.
