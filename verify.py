import nextcord
from nextcord import Interaction, SlashOption
from nextcord.ext import commands
import random
import string
import os
from dotenv import load_dotenv
from pymongo import MongoClient
import pymongo

cluster = MongoClient(f"mongodb+srv://theyseeguy:q8xTmBh8.Mm2a5@verification.pgbyxf6.mongodb.net/?retryWrites=true&w=majority")
db = cluster["Users"]
collection = db["verification"]

load_dotenv()
TOKEN = os.getenv("TOKEN")

intents = nextcord.Intents.default()
intents = nextcord.Intents.all()
bot = commands.Bot(intents=intents)

def ramdomNo():
    val = random.randint(1000, 9999)
    return str(val)

@bot.event
async def on_ready():
    print("Online!")

@bot.event
async def on_member_join(member):
    code = ramdomNo()
    mydict = {"_id": f"{member.id}", "Code": f"{code}", "Status": "Not verified"}
    x = collection.insert_one(mydict)

    await member.send(f"Welcome to ./xy! Verify yourself by typing your code in the <#1121151876646322256> channel: ||{code}||")


@bot.event
async def on_member_remove(member):
    collection.delete_one({"_id": f"{member.id}"})

    
@bot.slash_command()
async def verify(interaction: nextcord.Interaction, code: str):
    myquery = {"_id": f"{interaction.user.id}"}
    mydoc = collection.find(myquery)
    for x in mydoc:
        if code == x["Code"]:
            await interaction.response.send_message("Verified!", ephemeral=True)
            collection.update_one(myquery, {"$set": {"Status": "verified"}})
            role = nextcord.utils.get(interaction.guild.roles, name = "💠- verified")
            await interaction.user.add_roles(role)
            rmrole = nextcord.utils.get(interaction.guild.roles, name = "not_verified")
            await interaction.user.remove_roles(rmrole)
        
        else:
            await interaction.response.send_message("Not verified", ephemeral=True)

@bot.event
async def on_message():
    await message.

bot.run(TOKEN)
