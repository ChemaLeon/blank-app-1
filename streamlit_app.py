import json
from openai import OpenAI
import streamlit as st
from st_chat_message import message

client = OpenAI(
    api_key=st.secrets["api_key"]
)

system_prompt = """
You are a video game boss fighting a player.

Return ONLY JSON with:
player_damage
boss_damage
description

Example:
{
"player_damage": 12,
"boss_damage": 8,
"description": "The player slashes your armor dealing 12 damage and you strike back with a heavy claw. dealing 8 damage."
}
"""
with st.form('hp_form'):
    player_hp = (st.text_input("What should your health be? "))
    boss_hp = (st.text_input("What should the boss hp be? "))
    hp_button = st.form_submit_button("Submit starting hp")
    if hp_button:
        player_hp = int(player_hp)
        boss_hp = int(boss_hp)
        st.write('Hp set!')
if 'chat_history' not in st.session_state: 
    st.session_state['chat_history'] = [
                {"role": "system", "content": system_prompt},]

with st.form('attack'):
    button = st.form_submit_button('Submit')
    if type(player_hp) == int and player_hp > 0 and boss_hp > 0:
        attack = st.text_input("Describe your attack: ")
        
        if button:
            user_prompt = f"""
    Player HP: {player_hp}
    Boss HP: {boss_hp}

    The player attacks like this: {attack}

    Decide how much damage both sides take and describe the action.
    """

            st.session_state['chat_history'].append( {"role": "user", "content": user_prompt})
            response = client.chat.completions.create(
            model="gpt-4o",
            response_format= {'type':'json_object'},
            messages=st.session_state['chat_history'],
        
            )

            result = json.loads(response.choices[0].message.content)
            st.session_state['chat_history'].append({'role':'assistant','content':result['player_damage'] + result["boss_damage"] + result["description"]})
            player_hp -= result["boss_damage"]
            boss_hp -= result["player_damage"]

            message(result["description"],is_user=True)
            message(f"Player HP: {player_hp}")
            message(f"Boss HP: {boss_hp}")


    if player_hp <= 0:
        st.write("\nYou were defeated.")

    if boss_hp <= 0:
        st.write("\nYou defeated the boss!")






