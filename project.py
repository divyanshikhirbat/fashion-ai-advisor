import os
import customtkinter as ctk
import tkinter.filedialog as fd
from PIL import Image
import requests
import base64
import json
import io 

# =========================
# OPENROUTER API KEY
# =========================
OPENROUTER_API_KEY = "your_api_key_here"
# =========================
# APP WINDOW
# =========================
app = ctk.CTk()
app.geometry("1200x720")
app.title("Fashion AI Assistant")
ctk.set_appearance_mode("light")

# =========================
# BACKGROUND IMAGE
# =========================
base_dir = os.path.dirname(__file__)
img_path = os.path.join(base_dir, "assets", "background2.jpg")

bg_label = None
raw_bg_img = None

if os.path.exists(img_path):

    raw_bg_img = Image.open(img_path)

    bg_ctk_img = ctk.CTkImage(
        light_image=raw_bg_img,
        size=(1200, 720)
    )

    bg_label = ctk.CTkLabel(
        app,
        image=bg_ctk_img,
        text=""
    )

    bg_label.place(
        x=0,
        y=0,
        relwidth=1,
        relheight=1
    )

    bg_label.lower()

# =========================
# BACKGROUND RESIZE
# =========================
def resize_background(event):

    global raw_bg_img, bg_label

    if (
        event.widget == app
        and raw_bg_img
        and bg_label
    ):

        new_img = ctk.CTkImage(
            light_image=raw_bg_img,
            size=(event.width, event.height)
        )

        bg_label.configure(image=new_img)
        bg_label.image = new_img

app.bind("<Configure>", resize_background)

# =========================
# CURRENT MODE
# =========================
current_mode = "outfit"
uploaded_pil_image = None

# =========================
# MAIN CONTAINER
# =========================
parent_widget = bg_label if bg_label else app

main_container = ctk.CTkFrame(
    parent_widget,
    width=780,
    height=520,
    fg_color="#a178a2",
    corner_radius=25
)

main_container.place(
    relx=0.60,
    rely=0.5,
    anchor="center"
)

main_container.pack_propagate(False)

# =========================
# LEFT SIDE
# =========================
left_frame = ctk.CTkFrame(
    main_container,
    fg_color="transparent"
)

left_frame.pack(
    side="left",
    padx=(20, 10),
    pady=(45, 20)
)

image_label = ctk.CTkLabel(
    left_frame,
    text="No Image Uploaded",
    width=300,
    height=350,
    fg_color="#f4f4f4",
    text_color="black",
    corner_radius=20
)

image_label.pack(pady=(25,10))
# =========================
# RIGHT CHAT SECTION
# =========================

right_frame = ctk.CTkFrame(
    main_container,
    fg_color="transparent"
)

right_frame.pack(
    side="right",
    fill="both",
    expand=True,
    padx=(0, 20),
    pady=20
)

title_label = ctk.CTkLabel(
    right_frame,
    text="Fashion AI Stylist ✨",
    font=("Georgia", 28, "bold"),
    text_color="white"
)

title_label.pack(
    anchor="w",
    pady=(0, 12)
)

# =========================
# CHAT AREA
# =========================

chat_area = ctk.CTkScrollableFrame(
    right_frame,
    width=420,
    height=320,
    fg_color="#f7f2f7",
    corner_radius=18
)

chat_area.pack(
    fill="both",
    expand=True
)

# =========================
# MESSAGE FUNCTION
# =========================

def add_message(message, sender="ai"):

    bubble_color = "white"
    text_color = "black"
    bubble_anchor = "w"

    if sender == "user":
        bubble_color = "#620b5c"
        text_color = "white"
        bubble_anchor = "e"

    message_label = ctk.CTkLabel(
        chat_area,
        text=message,
        wraplength=240,
        justify="left",
        fg_color=bubble_color,
        text_color=text_color,
        corner_radius=22,
        padx=18,
        pady=14,
        font=("Segoe UI", 16)
    )

    message_label.pack(
        anchor=bubble_anchor,
        pady=8,
        padx=10
    )
    chat_area._parent_canvas.yview_moveto(1.0)

# starting AI message
add_message(
    "Hi✨ Upload an outfit or ask for styling help.",
    "ai"
)

# =========================
# INPUT SECTION
# =========================

input_frame = ctk.CTkFrame(
    right_frame,
    fg_color="transparent"
)

input_frame.pack(
    fill="x",
    pady=(10, 0)
)

user_input = ctk.CTkEntry(
    input_frame,
    placeholder_text="Type your fashion question...",
    height=45,
    corner_radius=20,
    font=("Segoe UI", 15)
)

user_input.pack(
    side="left",
    fill="x",
    expand=True,
    padx=(0, 10)
)

# =========================
# OCCASION DROPDOWN
# =========================

dropdown_values = [
 
]

occasion_dropdown = ctk.CTkComboBox(
    right_frame,
    values=dropdown_values,
    width=300,
    font=("Arial", 14),
    dropdown_font=("Arial", 13),
    fg_color="#f3dff1",
    text_color="#620b5c",
    button_color="#620b5c",
    border_color="#620b5c",
    corner_radius=10
)
# =========================
# SEND MESSAGE
# =========================
def send_message():

    global uploaded_pil_image

    user_text = user_input.get().strip()

    # =========================
    # HOME MODE
    # =========================

    if current_mode == "home":

        add_message(
            "Please select a feature first ✨",
            "ai"
        )

        return

    # =========================
    # EMPTY CHECK
    # =========================

    if user_text == "":
        return

    # =========================
    # SHOW USER MESSAGE
    # =========================

    add_message(user_text, "user")

    user_input.delete(0, "end")

    app.update()

    # =========================
    # IMAGE CHECK
    # =========================

    if uploaded_pil_image is None:

        add_message(
            "Please upload image first 📸",
            "ai"
        )

        return

    try:

        # =========================
        # IMAGE PROCESS
        # =========================

        original_img = uploaded_pil_image.copy()

        original_img = original_img.convert("RGB")

        original_img.thumbnail((512, 512))

        img_byte_arr = io.BytesIO()

        original_img.save(
            img_byte_arr,
            format="JPEG",
            quality=85
        )

        base64_image = base64.b64encode(
            img_byte_arr.getvalue()
        ).decode("utf-8")

        # =========================
        # PROMPT
        # =========================

        if current_mode == "critic":

            loading_msg = "Analyzing your outfit... 🎭✨"

            prompt_instructions = f"""
            You are an expert AI Outfit Critic.

            Analyze the uploaded outfit.

            User wants this aesthetic:
            {user_text}

            Give:
            - fitting improvements
            - posture tips
            - styling tricks
            - tuck/roll suggestions
            - aesthetic rating

            Keep the response short, stylish, and highly effective. Use only 4-6 concise bullet points with bold mini-headings in clean English.Do not use markdown symbols like ### or **.
            """

        elif current_mode == "occasion":

            loading_msg = f"Creating {user_text} styling ✨"

            prompt_instructions = f"""
            You are an AI Fashion Stylist.

            Create complete styling ideas
            for this occasion/style:

            {user_text}

            Suggest:
            - accessories
            - footwear
            - layering
            - hairstyle
            - fashion vibe

            Keep the response short, stylish, and highly effective. Use only 4-6 concise bullet points with bold mini-headings in clean English.Do not use markdown symbols like ### or **.
            """

        elif current_mode == "accessories":

            loading_msg = "Matching accessories... 💍✨"

            prompt_instructions = """
            Analyze the uploaded outfit.

            Suggest:
            - jewelry
            - bags
            - watches
            - makeup
            - hairstyles

            Keep the response short, stylish, and highly effective. Use only 4-6 concise bullet points with bold mini-headings in clean English.Do not use markdown symbols like ### or **.
            """

        else:

            loading_msg = "Analyzing outfit... 👗✨"

            prompt_instructions = """
            Analyze the uploaded outfit.

            Give:
            - outfit aesthetic
            - styling tips
            - color balance
            - celebrity inspiration
            - overall rating

            Keep the response short, stylish, and highly effective. Use only 4-6 concise bullet points with bold mini-headings in clean English.Do not use markdown symbols like ### or **.
            """

        # =========================
        # SHOW LOADING
        # =========================

        add_message(
            loading_msg,
            "ai"
        )

        app.update()

        # =========================
        # API
        # =========================

        API_URL = (
            "like here"
        )

        headers = {

            "Authorization":
            f"Bearer {OPENROUTER_API_KEY}",

            "Content-Type":
            "application/json"
        }

        payload = {

            "model":
            "openai/gpt-4o-mini",

            "max_tokens": 300,

            "messages": [

                {
                    "role": "user",

                    "content": [

                        {
                            "type": "text",
                            "text": prompt_instructions
                        },

                        {
                            "type": "image_url",

                            "image_url": {
                                "url":
                                f"data:image/jpeg;base64,{base64_image}"
                            }
                        }

                    ]
                }

            ]
        }

        # =========================
        # API REQUEST
        # =========================

        response = requests.post(
            API_URL,
            headers=headers,
            data=json.dumps(payload),
            timeout=60
        )

        print(response.text)

        # =========================
        # RESPONSE
        # =========================

        if response.status_code == 200:

            result = response.json()

            ai_response = (
                result["choices"][0]
                ["message"]["content"]
            )

            # sometimes response list format me aata hai
            if isinstance(ai_response, list):

                final_text = ""

                for item in ai_response:

                    if item.get("type") == "text":

                        final_text += item.get(
                            "text",
                            ""
                        )

                ai_response = final_text

            add_message(
                ai_response,
                "ai"
            )

        else:

            add_message(
                f"Server Error ({response.status_code})",
                "ai"
            )

            print(response.text)

    except Exception as e:

        add_message(
            f"Error: {str(e)}",
            "ai"
        )
         
            

send_button = ctk.CTkButton(
    input_frame,
    text="Send",
    command=send_message,
    width=90,
    height=45,
    corner_radius=20,
    fg_color="#620b5c",
    hover_color="#7a1173",
    font=("Segoe UI", 15, "bold")
)

send_button.pack(side="right")

# =========================
# UPDATE TEXT
# =========================
# =========================
# UPDATE TEXT
# =========================
def update_suggestion(text):

    # clear old widgets
    for widget in chat_area.winfo_children():
        widget.destroy()

    # =========================
    # HOME PAGE
    # =========================
    if current_mode == "home":

        home_label = ctk.CTkLabel(
            chat_area,
            text=text,
            wraplength=500,
            justify="center",
            font=("Times New Roman", 26, "italic"),
            text_color="#620b5c",
            fg_color="transparent"
        )

        home_label.pack(
            expand=True,
            fill="both",
            padx=30,
            pady=80
        )

    # =========================
    # NORMAL PAGES
    # =========================
    else:

        message_box = ctk.CTkLabel(
            chat_area,
            text=text,
            width=600,
            wraplength=500,
            justify="left",
            fg_color="white",
            text_color="#620b5c",
            corner_radius=20,
            padx=25,
            pady=25,
            font=("Trebuchet MS", 14, "bold")
        )

        message_box.pack(
            pady=20,
            padx=20,
            anchor="w"
        )

    # =========================
    # OCCASION BUTTONS
    # =========================
    if current_mode == "occasion":

        options = [
            "College Fest",
            "Airport Look",
            "Date Night",
            "Wedding",
            "Party",
            "Casual Outing"
        ]

        btn_frame = ctk.CTkFrame(
            chat_area,
            fg_color="transparent"
        )

        btn_frame.pack(
            pady=(5, 10),
            padx=10,
            fill="x"
        )

        for option in options:

            opt_btn = ctk.CTkButton(
                btn_frame,
                text=f"✨ {option}",
                font=("Segoe UI", 14),
                fg_color="#ffffff",
                text_color="#620b5c",
                border_color="#620b5c",
                border_width=1,
                hover_color="#f3dff1",
                corner_radius=15,
                height=40,

                command=lambda opt=option: [
                    user_input.delete(0, "end"),
                    user_input.insert(0, opt),
                    send_message()
                ]
            )

            opt_btn.pack(
                pady=6,
                fill="x",
                padx=20
            )

    # =========================
    # CRITIC BUTTONS
    # =========================
    if current_mode == "critic":

        critic_options = [
            "Korean fit critique",
            "Streetwear critique",
            "Old money critique",
            "Luxury fashion critique"
        ]

        critic_frame = ctk.CTkFrame(
            chat_area,
            fg_color="transparent"
        )

        critic_frame.pack(
            pady=(5, 10),
            padx=10,
            fill="x"
        )

        for option in critic_options:

            btn = ctk.CTkButton(
                critic_frame,
                text=f"🎭 {option}",
                font=("Segoe UI", 14),
                fg_color="#ffffff",
                text_color="#620b5c",
                border_color="#620b5c",
                border_width=1,
                hover_color="#f3dff1",
                corner_radius=15,
                height=40,

                command=lambda opt=option: [
                    user_input.delete(0, "end"),
                    user_input.insert(0, opt),
                    send_message()
                ]
            )

            btn.pack(
                pady=6,
                fill="x",
                padx=20
            )
# =========================
# SIDEBAR
# =========================
sidebar = ctk.CTkFrame(
    app,
    width=220,
    fg_color="#ffffff",
    corner_radius=0
)

sidebar.place(
    x=0,
    y=0,
    relheight=1
)

logo = ctk.CTkLabel(
    sidebar,
    text="FashionAI",
    font=("Arial", 24, "bold"),
    text_color="#620b5c"
)

logo.pack(pady=30)

# =========================
# ACTIVE BUTTON STYLE
# =========================
def reset_buttons():

    for btn in [
        home_btn,
        outfit_btn,
        accessory_btn,
        occasion_btn,
        critic_btn
   ]:

        btn.configure(
            fg_color="transparent",
            text_color="#620b5c"
        )


def build_final_prompt(user_text):

    style_map = {
        "Korean airport look":
            "Korean airport fashion, minimal neutral tones, oversized streetwear, Seoul street style, editorial photography",

        "Luxury party outfit":
            "luxury high fashion party outfit, glamorous evening dress, studio lighting, Vogue style",

        "Streetwear aesthetic":
            "urban streetwear, baggy clothes, sneakers, hip hop aesthetic, cinematic lighting",

        "Old money fashion":
            "old money aesthetic, elegant minimal luxury outfit, rich classy European fashion"
    }

    # if user clicked preset
    if user_text in style_map:
        style_prompt = style_map[user_text]

    else:
        # user custom demand
        style_prompt = f"fashion outfit based on: {user_text}"

    final_prompt = f"""
    Fashion try-on image of the same person in uploaded photo.
    Apply this style: {style_prompt}.
    Keep face, identity, pose consistent.
    High quality studio fashion photography, realistic lighting.
    """

    return final_prompt

# =========================
# HOME
# =========================
def show_home():
    global current_mode
    current_mode = "home"
    reset_buttons()
    for widget in chat_area.winfo_children():
        widget.destroy()
    
    # 1. Dropdown ko home page se hatane ke liye (Bina kisi error ke)
    if 'occasion_dropdown' in globals() and occasion_dropdown is not None:
        try:
            occasion_dropdown.pack_forget()
        except:
            pass

    # 2. Left upload panel aur bottom chat box ko hide karne ke liye
    try:
        left_frame.pack_forget()   
        input_frame.pack_forget()  
    except:
        pass

    # 3. Aapka soft and beautiful message
    home_message = (
        "✨ Welcome to AI Fashion Hub ✨\n"
        "Hey there! 👋\n\n"
        "Welcome to your space ✨.\n\n"
        "You’re doing great already 😊\n\n"
        "I am here to help you feel a little more confident and stylish 💛\n\n\n"
        "👉 Click any button on the left panel to explore!"
    )
    
    # Yeh automatically text ko bada aur colorful dikha dega naye logic se
    update_suggestion(home_message)
# =========================
# OUTFIT MODE
# =========================
def show_outfit():

    global current_mode
    current_mode = "outfit"
    reset_buttons()
    for widget in chat_area.winfo_children():
        widget.destroy()
    try:
        left_frame.pack(side="left", fill="both", expand=True)
        input_frame.pack(side="bottom", fill="x")
        # Agar koi dropdown open hai toh use safe hide karne ke liye
        occasion_dropdown.pack_forget()
    except:
        pass
    # ==========================================

    outfit_btn.configure(
        fg_color="#620b5c",
        text_color="white"
    )
    update_suggestion(
        "👗 Outfit Analyzer\n\n"
        "Upload your outfit image.\n\n"
        "AI will analyze:\n"
        "• Outfit aesthetic\n"
        "• Styling tips\n"
        "• Fashion rating\n"
        "• Celebrity inspiration\n"
        "• Better combinations"
    )
# =========================
# ACCESSORIES MODE
# =========================
def show_accessories():
    global current_mode

    current_mode = "accessories"

    reset_buttons()
    for widget in chat_area.winfo_children():
        widget.destroy()

    # ==========================================
    # GAYAB HUE UPLOAD BOX AUR SEND BAR KO WAPAS LAO
    # ==========================================
    try:
        left_frame.pack(side="left", fill="both", expand=True)
        input_frame.pack(side="bottom", fill="x")
        # Agar occasion dropdown dikh raha hai toh use hide karo
        if 'occasion_dropdown' in globals() and occasion_dropdown is not None:
            occasion_dropdown.pack_forget()
    except:
        pass
    # ==========================================

    accessory_btn.configure(
        fg_color="#620b5c",
        text_color="white"
    )
    update_suggestion(
        "💍 Accessories Match\n\n"
        "Upload an outfit image.\n\n"
        "AI will suggest:\n"
        "• Jewelry\n"
        "• Bags\n"
        "• Watches\n"
        "• Makeup style\n"
        "• Hairstyles"
    )
# =========================
# OCCASION OPTIONS
# =========================
def create_occasion_buttons():
    for widget in chat_area.winfo_children()[1:]:
        widget.destroy()

    options = [
        "College Fest",
        "Airport Look",
        "Date Night",
        "Wedding",
        "Party",
        "Casual Outing"
    ]

    btn_frame = ctk.CTkFrame(
        chat_area,
        fg_color="transparent"
    )

    btn_frame.pack(
        pady=10,
        padx=10,
        fill="x"
    )

    for option in options:

        opt_btn = ctk.CTkButton(
            btn_frame,
            text=f"✨ {option}",
            font=("Segoe UI", 14),
            fg_color="#ffffff",
            text_color="#620b5c",
            border_color="#620b5c",
            border_width=1,
            hover_color="#f3dff1",
            corner_radius=15,
            height=40,

            command=lambda opt=option: [
                user_input.delete(0, "end"),
                user_input.insert(0, opt),
                send_message()
            ]
        )

        opt_btn.pack(
            pady=6,
            fill="x",
            padx=20
        )

# =========================
# CRITIC OPTIONS
# =========================

def create_critic_buttons():
    for widget in chat_area.winfo_children()[1:]:
        widget.destroy()

    critic_options = [
        "Korean fit critique",
        "Streetwear critique",
        "Old money critique",
        "Luxury fashion critique"
    ]

    critic_frame = ctk.CTkFrame(
        chat_area,
        fg_color="transparent"
    )

    critic_frame.pack(
        pady=10,
        padx=10,
        fill="x"
    )

    for option in critic_options:

        btn = ctk.CTkButton(
            critic_frame,
            text=f"🎭 {option}",
            font=("Segoe UI", 14),
            fg_color="#ffffff",
            text_color="#620b5c",
            border_color="#620b5c",
            border_width=1,
            hover_color="#f3dff1",
            corner_radius=15,
            height=40,

            command=lambda opt=option: [
                user_input.delete(0, "end"),
                user_input.insert(0, opt),
                send_message()
            ]
        )

        btn.pack(
            pady=6,
            fill="x",
            padx=20
        )
# =========================
# OCCASION MODE
# =========================
def show_occasion():
    global current_mode
    current_mode = "occasion"

    reset_buttons()
    for widget in chat_area.winfo_children():
        widget.destroy()

    if not left_frame.winfo_ismapped():
        left_frame.pack(side="left", padx=(20, 10), pady=20)

    if not input_frame.winfo_ismapped():
        input_frame.pack(fill="x", pady=(10, 0))

    occasion_btn.configure(
        fg_color="#620b5c",
        text_color="white"
    )

    update_suggestion(
        "✨ Occasion Stylist ✨\n\n"
        "Choose your desired fashion aesthetic below 💖"
    )

    create_occasion_buttons()

# =========================
# CRITIC MODE
# =========================

def show_critic():
    global current_mode
    current_mode = "critic"

    reset_buttons()
    for widget in chat_area.winfo_children():
        widget.destroy()

    if not left_frame.winfo_ismapped():
        left_frame.pack(side="left", padx=(20, 10), pady=20)

    if not input_frame.winfo_ismapped():
        input_frame.pack(fill="x", pady=(10, 0))

    try:
        occasion_dropdown.pack_forget()
    except:
        pass

    critic_btn.configure(
        fg_color="#620b5c",
        text_color="white"
    )

    update_suggestion(
        "🎭 Outfit Critic\n\n"
        "Select a fashion vibe below and AI will brutally\n"
        "critique your current fit ✨"
    )

    critic_options = [
        "Korean fit critique",
        "Streetwear critique",
        "Old money critique",
        "Luxury fashion critique"
    ]

    create_critic_buttons()

# =========================
# BUTTONS
# =========================
home_btn = ctk.CTkButton(
    sidebar,
    text="Home",
    command=show_home,
    fg_color="transparent",
    hover_color="#f3dff1",
    text_color="#620b5c",
    font=("Arial", 14, "bold")
)

home_btn.pack(
    pady=8,
    padx=20,
    fill="x"
)

outfit_btn = ctk.CTkButton(
    sidebar,
    text="Outfit Analyzer ✨",
    command=show_outfit,
    fg_color="transparent",
    hover_color="#f3dff1",
    text_color="#620b5c",
    font=("Arial", 14, "bold")
)

outfit_btn.pack(
    pady=8,
    padx=20,
    fill="x"
)

accessory_btn = ctk.CTkButton(
    sidebar,
    text="Accessories Match 💍",
    command=show_accessories,
    fg_color="transparent",
    hover_color="#f3dff1",
    text_color="#620b5c",
    font=("Arial", 14, "bold")
)

accessory_btn.pack(
    pady=8,
    padx=20,
    fill="x"
)

occasion_btn = ctk.CTkButton(
    sidebar,
    text="Occasion Looks 👗",
    command=show_occasion,
    fg_color="transparent",
    hover_color="#f3dff1",
    text_color="#620b5c",
    font=("Arial", 14, "bold")
)

occasion_btn.pack(
    pady=8,
    padx=20,
    fill="x"
)
critic_btn = ctk.CTkButton(
    sidebar,
    text="Outfit Critic 🎭",
    command=show_critic,
    fg_color="transparent",
    hover_color="#f3dff1",
    text_color="#620b5c",
    font=("Arial", 14, "bold")
)

critic_btn.pack(
    pady=8,
    padx=20,
    fill="x"
)

# =========================
# AI ANALYSIS
# =========================
def get_prompt():

    if current_mode == "outfit":

        return (
            "Analyze this outfit professionally.\n"
            "Tell:\n"
            "1. Outfit aesthetic\n"
            "2. Best styling tips\n"
            "3. Footwear suggestions\n"
            "4. Fashion rating\n"
            "5. Celebrity inspiration"
        )

    elif current_mode == "accessories":

        return (
            "Analyze this outfit and suggest:\n"
            "1. Jewelry\n"
            "2. Bags\n"
            "3. Watches\n"
            "4. Makeup style\n"
            "5. Hairstyle"
        )

    elif current_mode == "occasion":

        return (
            "Analyze this outfit for occasions.\n"
            "Tell:\n"
            "1. Best occasion to wear it\n"
            "2. How to improve it for parties\n"
            "3. How to make it look luxurious\n"
            "4. Matching colors\n"
            "5. Final styling advice"
        )

    return "Analyze this fashion image."

# =========================
# IMAGE UPLOAD
# =========================
def upload_image():

    global uploaded_pil_image

    file_path = fd.askopenfilename(
        filetypes=[
            ("Images", "*.jpg *.jpeg *.png *.webp")
        ]
    )

    if not file_path:
        return
    img = Image.open(file_path).convert("RGB").copy()
    uploaded_pil_image = img

    # =========================
    # IMAGE PREVIEW
    # =========================

    display_img = ctk.CTkImage(
        light_image=img,
        size=(300, 350)
    )

    image_label.configure(
        image=display_img,
        text=""
    )

    image_label.image = display_img
    image_label.current_file = file_path

    add_message("New outfit uploaded ✨", "ai")

    # =========================
    # OCCASION / CRITIC
    # =========================

    if current_mode == "occasion":

     add_message(
        "✨ Image uploaded successfully!\nNow select an occasion below 💖",
        "ai"
    )

    create_occasion_buttons()

    if current_mode == "critic":

      add_message(
        "✨ Image uploaded successfully!\nNow select a critique style below 🎭",
        "ai"
    )

    create_critic_buttons()


    # =========================
    # AUTO ANALYZE
    # =========================

    update_suggestion(
        "Fashion AI is analyzing... ✨"
    )

    app.update()

    try:

        with open(file_path, "rb") as image_file:

            encoded_string = base64.b64encode(
                image_file.read()
            ).decode("utf-8")

        headers = {

            "Authorization":
            f"Bearer {OPENROUTER_API_KEY}",

            "Content-Type":
            "application/json"
        }

        # =========================
        # PROMPT
        # =========================

        if current_mode == "accessories":

            prompt_text = """
            Analyze this outfit carefully.

            Suggest:
            • Jewelry
            • Bags
            • Watches
            • Makeup
            • Hairstyle

            Keep response short and stylish.
            """

        else:

            prompt_text = """
            Analyze this fashion outfit carefully.

            Give:
            • Outfit aesthetic
            • Styling tips
            • Color balance
            • Celebrity inspiration
            • Fashion rating

            Keep response short and stylish.
            """

        payload = {

            "model":
            "openai/gpt-4o-mini",

            "max_tokens": 200,

            "messages": [
                {
                    "role": "user",

                    "content": [

                        {
                            "type": "text",
                            "text": prompt_text
                        },

                        {
                            "type": "image_url",

                            "image_url": {
                                "url":
                                f"data:image/jpeg;base64,{encoded_string}"
                            }
                        }

                    ]
                }
            ]
        }

        response = requests.post(

            "like here",

            headers=headers,

            data=json.dumps(payload),

            timeout=60
        )

        res_json = response.json()

        if "choices" in res_json:

            ai_reply = (
                res_json["choices"][0]
                ["message"]["content"]
            )

            add_message(ai_reply, "ai")

        elif "error" in res_json:

            add_message(
                f"API Error:\n{res_json['error']['message']}",
                "ai"
            )

        else:

            add_message(
                f"Unexpected Error:\n{res_json}",
                "ai"
            )

    except Exception as e:

        add_message(
            f"System Error:\n{str(e)}",
            "ai"
        )

    # =========================
    # OPEN IMAGE
    # =========================

    #img = Image.open(file_path).convert("RGB").copy()

    uploaded_pil_image = img

    # =========================
    # IMAGE PREVIEW
    # =========================

    display_img = ctk.CTkImage(
        light_image=img,
        size=(300, 350)
    )

    image_label.configure(
        image=display_img,
        text=""
    )

    image_label.image = display_img
    image_label.current_file = file_path

    add_message("New outfit uploaded ✨", "ai")

    # =========================
    # OCCASION / CRITIC
    # =========================

    if current_mode in ["occasion", "critic"]:

        add_message(
            "✨ Image uploaded successfully!\nNow select a style option below 💖",
            "ai"
        )

    # =========================
    # AUTO ANALYZE
    # =========================

    update_suggestion(
        "Fashion AI is analyzing... ✨"
    )

    app.update()

    try:

        with open(file_path, "rb") as image_file:

            encoded_string = base64.b64encode(
                image_file.read()
            ).decode("utf-8")

        headers = {

            "Authorization":
            f"Bearer {OPENROUTER_API_KEY}",

            "Content-Type":
            "application/json"
        }

        # =========================
        # PROMPT
        # =========================

        if current_mode == "accessories":

            prompt_text = """
            Analyze this outfit carefully.

            Suggest:
            • Jewelry
            • Bags
            • Watches
            • Makeup
            • Hairstyle

            Give stylish and aesthetic fashion advice
            Keep the response short, stylish, and highly effective. Use only 4-6 concise bullet points with bold mini-headings in clean English.Do not use markdown symbols like ### or **.
            """

        else:

            prompt_text = """
            Analyze this fashion outfit carefully.

            Give:
            • Outfit aesthetic
            • Styling tips
            • Color balance
            • Celebrity inspiration
            • Fashion rating

            Give stylish and aesthetic fashion advice
            Keep the response short, stylish, and highly effective. Use only 4-6 concise bullet points with bold mini-headings in clean English.Do not use markdown symbols like ### or **.
            """

        # =========================
        # API PAYLOAD
        # =========================

        payload = {

            "model":
            "openai/gpt-4o-mini",

            "max_tokens": 200,

            "messages": [
                {
                    "role": "user",

                    "content": [

                        {
                            "type": "text",
                            "text": prompt_text
                        },

                        {
                            "type": "image_url",

                            "image_url": {
                                "url":
                                f"data:image/jpeg;base64,{encoded_string}"
                            }
                        }

                    ]
                }
            ]
        }

        # =========================
        # API REQUEST
        # =========================

        response = requests.post(

            "like here",

            headers=headers,

            data=json.dumps(payload),

            timeout=60
        )

        res_json = response.json()

        print(res_json)

        # =========================
        # RESPONSE
        # =========================

        if "choices" in res_json:

            ai_reply = (
                res_json["choices"][0]
                ["message"]["content"]
            )

            add_message(ai_reply, "ai")

        elif "error" in res_json:

            update_suggestion(
                f"API Error:\n\n"
                f"{res_json['error']['message']}"
            )

        else:

            update_suggestion(
                f"Unexpected Error:\n\n{res_json}"
            )

    except Exception as e:

        update_suggestion(
            f"System Error:\n\n{str(e)}"
        )
# =========================
# UPLOAD BUTTON
# =========================
upload_button = ctk.CTkButton(
    left_frame,
    text="Upload Outfit ✨",
    command=upload_image,
    fg_color="#620b5c",
    hover_color="#8b2d83",
    text_color="white",
    font=("Arial", 15, "bold"),
    corner_radius=25,
    width=200,
    height=45
)

upload_button.pack(pady=15)

# =========================
# START
# =========================
current_mode = "home"
show_home()
app.mainloop()