def recommend_hotel(merged_data, city, budget, duration):
    city = city.lower()
    
    # Filter for the given city
    city_hotels = merged_data[merged_data['City'] == city]
    
    if city_hotels.empty:
        return f"No hotels found for city: {city.capitalize()}"
    
    # Calculate price range
    min_price = budget * 0.8
    max_price = budget * 1.2
    
    # Filter by price range
    price_filtered_hotels = city_hotels[
        (city_hotels['Hotel_Price'] >= min_price) & 
        (city_hotels['Hotel_Price'] <= max_price)
    ]
    
    if price_filtered_hotels.empty:
        return f"No hotels found in {city.capitalize()} within the price range: {min_price} - {max_price}"
    
    # Recommend the top-rated hotel
    recommended_hotel_name = price_filtered_hotels.sort_values(by='Hotel_Rating', ascending=False)['Hotel_Name'].iloc[0]
    
    return recommended_hotel_name
