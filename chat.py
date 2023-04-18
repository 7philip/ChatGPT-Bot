from tkinter import *
import customtkinter
import openai
import os
import pickle

#App initiation codes
root = customtkinter.CTk()
root.title("ChatGPT Philbot")
root.geometry("600x500")
root.iconbitmap('ai_lt.ico') #https://tkinter.com/ai_lt.ico

#Setting color scheme
customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")  # Themes: "blue" (standard), "green", "dark-blue"

#Submit to ChatGPT
def speak():
	if chat_entry.get():

			#Define filename
			filename = "api_key"
			try: #error handling line begins

				if os.path.isfile(filename):
					# Open the file
					input_file = open(filename, 'rb')

					#Loading the data from file into a variable
					stuff = pickle.load(input_file)

					#*******************************Something different from def key()********************************
					# Query ChatGPT
					#resp_text.insert(END, "Working..........") #sampling if there is response

					#Defining API key
					openai.api_key = stuff

					#Creating an instance
					openai.Model.list()

					# Defining our query response
					response = openai.Completion.create(
						model = "text-davinci-003",
						prompt = chat_entry.get(),
						temperature = 0,
						max_tokens = 60,
						top_p = 1.0,
						frequency_penalty=0.0,
						presence_penalty=0.0
						)

					resp_text.insert(END, (response["choices"][0]["text"]).strip())
					resp_text.insert(END, "\n\n")





				else:
					# create the file
					input_file = open(filename, 'wb')

					#close file into a variable
					input_file.close()
					#Error message if key is missing
					resp_text.insert(END, f"\n\nOops, you need an API Key to speak to ChatGPT. Get one from here:\nhttps://beta.openai.com/account/api-keys")


			except Exception as e: #error handli line ends
				resp_text.insert(END, f"\n\n Oops, there was an error \n\n{e}")

	else:
		resp_text.insert(END, f"\n\n Oops, there was an error \n\n{e}")




#clear the screen
def clear():
	#Clear the main text box
	resp_text.delete(1.0, END)
	#Clear query entry box
	chat_entry.delete(0, END)


#AI Key and stuff

def key():

	#Define filename
	filename = "api_key"
	try: #error handling line begins

		if os.path.isfile(filename):
			# Open the file
			input_file = open(filename, 'rb')

			#Loading the data from file into a variable
			stuff = pickle.load(input_file)

			#output the file content to entry box
			api_entry.insert(END, stuff)
		else:
			# create the file
			input_file = open(filename, 'wb')

			#close file into a variable
			input_file.close()
	except Exception as e: #error handli line ends
		resp_text.insert(END, f"\n\nOops, there was an error \n\n{e}")


	#Resize app to Large
	root.geometry('600x650')
	#Show API Frame
	api_frame.pack(pady=30)

	



def save_key():
	# Defining filename
	filename = "api_key"


	try:

		
		#output file
		output_file = open(filename, 'wb')

		#Actually add the data to the file
		pickle.dump(api_entry.get(), output_file)

		# delete entry box
		api_entry.delete(0, END)
		#Hide API frame
		api_frame.pack_forget()
		# Resize App to small
		root.geometry('600x500')

	except Exception as e: #error handli line ends
		resp_text.insert(END, f"\n\n Oops, there was an error \n\n{e}")


#creating main frame for program
text_frame = customtkinter.CTkFrame(root)
text_frame.pack(pady=20)

#Adding text widget to get ChatGPT reponses
resp_text = Text(text_frame,
	bg="#343638",
	width= 65,
	bd= 1,
	fg="#d6d6d6",
	wrap=WORD,
	selectbackground="#1f538d"
	)

resp_text.grid(row=0, column=0)

# create CTk scrollbar
ctk_textbox_scrollbar = customtkinter.CTkScrollbar(text_frame, command=resp_text.yview)
ctk_textbox_scrollbar.grid(row=0, column=1, sticky="ns")

# connect textbox scroll event to CTk scrollbar
resp_text.configure(yscrollcommand=ctk_textbox_scrollbar.set)

chat_entry = customtkinter.CTkEntry(root, placeholder_text="Type something to my custom bot....",
	width=535,
	height=50,
	border_width = 1
	)
chat_entry.pack(pady=10)


#creating submitbuttons
button_frame = customtkinter.CTkFrame(root, fg_color="#242424")
button_frame.pack(pady=10)

submit_button = customtkinter.CTkButton(button_frame, text="Speak to ChatGPT", command=speak)
submit_button.grid(row=0, column=0, padx=25)

clear_button = customtkinter.CTkButton(button_frame, text="Clear ChatGPT response", command=clear)
clear_button.grid(row=0, column=1, padx=35)

api_button = customtkinter.CTkButton(button_frame, text="Update API", command=key)
api_button.grid(row=0, column=2, padx=25)

#Add API Key Frame
api_frame = customtkinter.CTkFrame(root, border_width=1)
api_frame.pack(pady=30)

# API Entry widget

api_entry = customtkinter.CTkEntry(api_frame, placeholder_text="Enter your API Key.",
	width=350,
	height=50,
	border_width = 1
	)
api_entry.grid(row=0, column=0, padx=20, pady=20)

# Add API button

api_save_button = customtkinter.CTkButton(api_frame, text="Save Key", command=save_key)
api_save_button.grid(row=0, column=1, padx=10)



root.mainloop()