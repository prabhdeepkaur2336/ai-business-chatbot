# app.py - WORKING VERSION WITH YOUR JSON
import streamlit as st
import json
import random
from datetime import datetime

# ========== CONFIGURATION ==========
st.set_page_config(
    page_title="AI Business Assistant",
    page_icon="🤖",
    layout="wide"
)

# ========== LOAD BUSINESS DATA ==========
@st.cache_data
def load_business_data():
    try:
        with open('business_data.json', 'r') as f:
            return json.load(f)
    except Exception as e:
        st.error(f"Error loading JSON: {str(e)}")
        return {
            "business_name": "AI Solutions Co.",
            "business_type": "E-commerce"
        }

business = load_business_data()
BUSINESS_NAME = business.get('business_name', 'AI Solutions Co.')
BUSINESS_TYPE = business.get('business_type', 'E-commerce')

# ========== AI RESPONSE ENGINE ==========
def get_ai_response(user_input):
    """Smart responses based on your business_data.json"""
    
    input_lower = user_input.lower()
    
    # 1. GREETINGS
    if any(word in input_lower for word in ['hi', 'hello', 'hey', 'namaste']):
        greetings = [
            f"Hello! Welcome to {BUSINESS_NAME}! How can I help? 🤗",
            f"Hi there! I'm your AI assistant for {BUSINESS_NAME}. What can I do for you?",
            f"Welcome to {BUSINESS_NAME}! Ready to assist you!"
        ]
        return random.choice(greetings)
    
    # 2. SERVICES
    if any(word in input_lower for word in ['service', 'offer', 'provide', 'what do you do']):
        services = business.get('services', [])
        if services and isinstance(services, list):
            response = "**Our Services:**\n\n"
            for service in services:
                name = service.get('name', 'Service')
                price = service.get('price', 'Contact for price')
                time = service.get('delivery_time', 'Contact for time')
                response += f"• **{name}** - {price} (Delivery: {time})\n"
            return response
    
    # 3. PRICING
    if any(word in input_lower for word in ['price', 'cost', 'how much', 'rate']):
        services = business.get('services', [])
        if services and isinstance(services, list):
            # Find minimum price
            prices = []
            for service in services:
                price_str = service.get('price', '₹0')
                try:
                    price_num = int(price_str.replace('₹', '').replace(',', ''))
                    prices.append(price_num)
                except:
                    pass
            
            if prices:
                min_price = min(prices)
                return f"Our services start from **₹{min_price:,}**. Which service are you interested in?"
    
    # 4. PRODUCTS
    if any(word in input_lower for word in ['product', 'item', 'sell', 'buy']):
        products = business.get('products', [])
        if products and isinstance(products, list):
            response = "**Our Products:**\n\n"
            for product in products[:3]:  # Show first 3
                name = product.get('name', 'Product')
                price = product.get('price', '₹0')
                response += f"• **{name}** - {price}\n"
            return response
    
    # 5. CONTACT
    if any(word in input_lower for word in ['contact', 'call', 'email', 'phone', 'reach']):
        contact = business.get('contact', {})
        if contact and isinstance(contact, dict):
            response = "**Contact Information:**\n"
            for key, value in contact.items():
                response += f"• **{key.title()}**: {value}\n"
            return response
    
    # 6. DELIVERY
    if any(word in input_lower for word in ['delivery', 'shipping', 'time', 'how long']):
        # Check for delivery in products
        products = business.get('products', [])
        if products and isinstance(products, list):
            for product in products:
                if 'delivery' in product:
                    return f"Delivery for {product.get('name')}: {product.get('delivery')}"
        
        # Check business hours
        hours = business.get('business_hours', {})
        if hours:
            return f"**Business Hours:**\n• Weekdays: {hours.get('weekdays')}\n• Weekends: {hours.get('weekends')}"
    
    # 7. FAQS
    if 'faqs' in business:
        faqs = business.get('faqs', [])
        for faq in faqs:
            if isinstance(faq, dict):
                question = faq.get('question', '').lower()
                if question and question in input_lower:
                    return faq.get('answer', 'Please contact us for details.')
    
    # 8. DEFAULT RESPONSE
    default_responses = [
        f"I can help you with information about {BUSINESS_NAME}. Try asking about our services, products, or contact details!",
        f"Looking for information about {BUSINESS_TYPE} services? I'm here to help!",
        "Great question! Could you be more specific so I can assist you better?",
        f"Visit {BUSINESS_NAME}'s website or contact us directly for detailed assistance."
    ]
    return random.choice(default_responses)

# ========== STREAMLIT UI ==========
st.title(f"🤖 {BUSINESS_NAME} AI Assistant")
st.caption(f"Your 24/7 {BUSINESS_TYPE} Assistant | Secure • Fast • Reliable")

# Sidebar with Business Info
with st.sidebar:
    st.header(f"About {BUSINESS_NAME}")
    st.write(f"**Type:** {BUSINESS_TYPE}")
    st.write(f"**Tagline:** {business.get('tagline', 'Automating Business Solutions')}")
    
    # Contact Info
    contact = business.get('contact', {})
    if contact:
        st.divider()
        st.subheader("📞 Contact")
        for key, value in contact.items():
            st.write(f"**{key.title()}:** {value}")
    
    # Pricing Info
    services = business.get('services', [])
    if services and isinstance(services, list):
        st.divider()
        st.subheader("💰 Pricing")
        
        # Find minimum price
        prices = []
        for service in services:
            price_str = service.get('price', '₹0')
            try:
                price_num = int(price_str.replace('₹', '').replace(',', ''))
                prices.append(price_num)
            except:
                pass
        
        if prices:
            min_price = min(prices)
            st.metric("Starting Price", f"₹{min_price:,}", "+0%")
    
    st.divider()
    
    # Action Buttons
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🚀 Order", use_container_width=True):
            st.success("Basic Chatbot: ₹2,500\nDelivery: 24 hours")
    
    with col2:
        if st.button("📞 Call", use_container_width=True):
            st.info("Call: 1800-123-4567")

# Main Chat Interface
col1, col2 = st.columns([2, 1])

with col1:
    # Chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []
        # Welcome message
        st.session_state.messages.append({
            "role": "assistant",
            "content": f"Hello! I'm your AI assistant for **{BUSINESS_NAME}**. I can help with:\n• Service information\n• Product details\n• Pricing\n• Contact info\n\nHow can I assist you today? 😊"
        })
    
    # Display chat
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Chat input
    if prompt := st.chat_input(f"Ask about {BUSINESS_TYPE}..."):
        # Add user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Get AI response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = get_ai_response(prompt)
                st.markdown(response)
        
        # Add to history
        st.session_state.messages.append({"role": "assistant", "content": response})

with col2:
    # Business Dashboard
    st.header("📊 Business Dashboard")
    
    # Quick Stats
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Chats Today", "47", "+12%")
    with col2:
        st.metric("Response Time", "1.8s", "-0.4s")
    
    # Services Preview
    st.subheader("🎯 Top Services")
    services = business.get('services', [])
    if services and isinstance(services, list):
        for service in services[:2]:  # Show 2 services
            with st.expander(f"{service.get('name')} - {service.get('price')}"):
                features = service.get('features', [])
                for feature in features[:3]:  # Show 3 features
                    st.write(f"✓ {feature}")
    
    # Products Preview
    st.subheader("🛍️ Top Products")
    products = business.get('products', [])
    if products and isinstance(products, list):
        for product in products[:2]:  # Show 2 products
            st.write(f"**{product.get('name')}**")
            st.caption(f"Price: {product.get('price')}")
            st.caption(f"Stock: {product.get('stock', 'In stock')}")
            st.divider()
    
    # Quick Actions
    st.subheader("⚡ Quick Actions")
    
    action_col1, action_col2 = st.columns(2)
    with action_col1:
        if st.button("📦 Products"):
            st.session_state.messages.append({"role": "user", "content": "Show me your products"})
            st.rerun()
    
    with action_col2:
        if st.button("💰 Prices"):
            st.session_state.messages.append({"role": "user", "content": "What are your prices?"})
            st.rerun()
    
    if st.button("🛒 Order Now", type="primary", use_container_width=True):
        st.session_state.messages.append({"role": "user", "content": "I want to place an order"})
        st.rerun()

# Footer
st.divider()
st.caption(f"© {datetime.now().year} {BUSINESS_NAME}. All rights reserved. | 🔒 Secure | ⚡ Fast | 🔄 Live")

# Add testimonials if available
testimonials = business.get('testimonials', [])
if testimonials:
    st.divider()
    st.subheader("🌟 Customer Testimonials")
    
    cols = st.columns(min(3, len(testimonials)))
    for idx, testimonial in enumerate(testimonials[:3]):
        with cols[idx % 3]:
            st.info(f"\"{testimonial.get('review', '')}\"\n\n— **{testimonial.get('name', 'Customer')}**, {testimonial.get('business', 'Business')}")