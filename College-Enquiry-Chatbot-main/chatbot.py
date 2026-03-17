context = {}

def chatbot_response(user_input):
    global context
    user_input = user_input.lower().strip()

    # -------- HELLO -------- #
    if any(word in user_input for word in ["hello", "hi", "hey"]):
        return """Hi 👋 Welcome to Indo Global College Bot!

You can ask me about:
👉 College Information  
👉 Engineering Courses  
👉 Fee Structure  
👉 Principal / Dean  
👉 Hostel & Transport  
👉 Placements  

Try asking:
- fees for btech
- who is principal
- courses available
"""

    # -------- PRINCIPAL FLOW -------- #
    if context.get("ask_principal"):
        if "engineering" in user_input:
            context["ask_principal"] = False
            return "👩‍🏫 Engineering Principal: Dr. Promila Kaushal"

        elif "management" in user_input:
            context["ask_principal"] = False
            return "👨‍🏫 Management Principal: Dr. S P Ahuja"

        else:
            return "❓ Please choose: Engineering or Management"

    if "principal" in user_input or "principle" in user_input:
        context["ask_principal"] = True
        return "Which principal do you want?\n👉 Engineering\n👉 Management"

    # -------- COLLEGE INFO -------- #
    if "college information" in user_input or "about college" in user_input:
        return """Indo Global Group of Colleges, Mohali is a leading institution established in 2003.
Located in Abhipur near Chandigarh, it provides a green campus environment.
It is affiliated with IKGPTU and approved by AICTE.
Offers Engineering, Management and other programs.
Focuses on quality education and placements."""

    if "name" in user_input:
        return "Indo Global Group of Colleges, Abhipur, Mohali."

    if "location" in user_input or "where" in user_input:
        return "📍 Located in Abhipur, Mohali, Punjab."

    if "chairman" in user_input:
        return "👑 Chairman: Mr. Sukhdev Singh"

    if "dean" in user_input:
        return "🎓 Dean: Dr. Hardeep Singh Saini"

    # -------- COURSES -------- #
    if "course" in user_input or "engineering courses" in user_input:
        return """💻 Engineering Courses:
- Computer Science
- Mechanical
- Civil
- Electrical
- Electronics

Duration: 4 Years"""

    # -------- FEES -------- #
    if "fee" in user_input:
        return """💰 Fee Structure (Approx):

B.Tech:
- Tuition Fee: ₹70,000 – ₹90,000/year  

Hostel:
- Hostel Fee: ₹60,000 – ₹80,000/year  

Transport:
- Bus Fee: ₹20,000 – ₹30,000/year
"""

    # -------- HOSTEL FEE (IMPORTANT ORDER) -------- #
    if "hostel fee" in user_input:
        return """🏠 Hostel Fee:

- ₹60,000 – ₹80,000 per year  
👉 Includes accommodation & basic facilities."""

    # -------- HOSTEL -------- #
    if "hostel" in user_input:
        return "🏠 Hostel available for boys and girls with good facilities."

    # -------- TRANSPORT -------- #
    if "transport" in user_input or "bus" in user_input:
        return "🚌 Transport facility available."

    # -------- PLACEMENT -------- #
    if "placement" in user_input or "company" in user_input:
        return """💼 Placement Companies:

- Infosys  
- Wipro  
- TCS  
- HCL  
- IBM  
- Capgemini  
- Tech Mahindra  

👉 Training & placement support provided."""

    # -------- LPA -------- #
    if "lpa" in user_input or "package" in user_input or "salary" in user_input:
        return """💰 Placement Package (Approx):

- Average Package: 3 – 5 LPA  
- Highest Package: 8 – 12 LPA  

👉 Depends on student skills & company."""

    # -------- DEFAULT -------- #
    return "❗ Sorry, I don't have information about that. Please ask about fees, courses, placements, or college details."