import json
from openai import OpenAI
import streamlit as st

client = OpenAI(
    api_key=st.secrets["api_key2"]
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
    hp_player = st.text_input("What should your health be? ")
    hp_boss = st.text_input("What should the boss hp be? ")
    difficuly = st.text_input("Submit the difficulty(easy, meduim, hard, master) ")
    bosstype = st.text_input("What should the boss be? ")
    submit_button = st.form_submit_button("Submit starting inputs")

    if submit_button:
        if 'player_hp' not in st.session_state:
            st.session_state['difficulty'] = difficuly
            st.session_state['bosstype'] = bosstype
            st.session_state['player_hp'] = hp_player
            st.session_state['boss_hp'] = hp_boss
        st.write(f'Hp set! {st.session_state['player_hp']}')
if 'chat_history' not in st.session_state: 
    st.session_state['chat_history'] = [
                {"role": "system", "content": system_prompt},]

with st.form('attack'):
    button = st.form_submit_button('Submit')
    if 'player_hp' in st.session_state and 'boss_hp' in st.session_state and st.session_state['player_hp'] > '0' and st.session_state['boss_hp'] > '0':
        attack = st.text_input("Describe your attack: ")
        
        if button:
            user_prompt = f"""
    Player HP: {st.session_state['player_hp']}
    Boss HP: {st.session_state['boss_hp']}

    The player attacks like this: {attack}
    As you the boss, you are a {st.session_state['bosstype']}
    and with the difficulty as{st.session_state['difficulty']}

    if the player or you chooses to dodge or block the attack choose a number 10-100 and cancle that percent of damage such as 60 and you cancel 60% of the damage with the block or dodge. 

    !!cheat code!!
    if the player types "you dont want to make me angry", their damage is multiplied by 10 and their attacks are undodgeable.
    Decide how much damage both sides take and describe the action.
    """

            st.session_state['chat_history'].append( {"role": "user", "content": user_prompt})
            response = client.chat.completions.create(
            model="gpt-4o",
            response_format= {'type':'json_object'},
            messages=st.session_state['chat_history'],
        
            )

            result = json.loads(response.choices[0].message.content)
            st.session_state['chat_history'].append({'role':'assistant','content':str(result['player_damage']) + str(result["boss_damage"]) + result["description"]})
            st.session_state['player_hp'] = str(int(st.session_state['player_hp'])- result["boss_damage"])
            st.session_state['boss_hp'] = str(int(st.session_state['boss_hp'])- result["player_damage"])

            with st.chat_message("user"):
                st.write(result["description"])
            with st.chat_message('ai'):

                st.write(f"Player HP: {st.session_state['player_hp']}")
                st.write(f"Boss HP: {st.session_state['boss_hp']}")

    if 'player_hp' in st.session_state and 'boss_hp' in st.session_state:
        if st.session_state['player_hp'] <= '0':
            st.write("\nYou were defeated.")

        if st.session_state['boss_hp'] <= '0':
            st.write("\nYou defeated the boss!")






