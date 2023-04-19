#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 12 20:26:03 2020

@author: vboxuser
"""
import torch, argparse
from load_configs import model, tokenizer, opts, device, p1_tok, p2_tok, act_tok, start_tok
from utilsss import *

action_space = [ 'ask about kids.', "ask about pets.", 'talk about work.', 
               'ask about marital status.', 'talk about travel.', 'ask about age and gender.',
        'ask about hobbies.', 'ask about favorite food.', 'talk about movies.', 
        'talk about music.', 'talk about politics.']


def generate_next(bot_input_ids, do_sample=True, top_k=10, top_p=.92,
                  max_length=1000, pad_token=tokenizer.eos_token_id):
    full_msg = model.generate(bot_input_ids, do_sample=True,
                                              top_k=top_k, top_p=top_p, 
                                              max_length=max_length, pad_token_id=tokenizer.eos_token_id)
    msg = to_data(full_msg.detach()[0])[bot_input_ids.shape[-1]:]
    return msg

## Interactive Mode w/ User ##
def get_personas():
    # custom personas for conversation

    # >> Fact 1: I love sitting at home all days
    # >> Fact 2: Every day I study new thing about this worls
    # >> Fact 3: I want to help people be happier
    # >> Fact 4: Someday I can change this world upside down
    # >> Fact 5: My hobbyies skateboarding and programming    

    personas = [50261, 40, 1842, 5586, 379, 1363, 477, 1528, 50256, 6109, 1110, 314, 2050, 649, 1517, 546, 428, 476, 7278, 50256, 40, 765, 284, 1037, 661, 307, 23030, 50256, 50, 12657, 323, 314, 460, 1487, 428, 995, 17196, 866, 50256, 3666, 20005, 444, 22647, 27794, 290, 8300, 50256, 50257, 50259]
    return personas

def interact(choice, personas, text_input, length=8, top_k=10, top_p=.92, max_length=1000):
    dialog_hx = []

    # chat time
    for step in range(1):
        if choice ==1:
            # encode the user input
            user_inp = tokenizer.encode(text_input + tokenizer.eos_token)
            # append to the chat history
            dialog_hx.append(user_inp)
                
            # generated a response while limiting the total chat history to 1000 tokens, 
            bot_input_ids = to_var([personas + flatten(dialog_hx)]).long()
            msg = generate_next(bot_input_ids, top_k=top_k, top_p=top_p, max_length=max_length)
            dialog_hx.append(msg)
            # print("Bot: {}".format(tokenizer.decode(msg, skip_special_tokens=True)))

        else:
            act = None
            while act not in action_space:
                display_dialog_history(dialog_hx)
                print()
                print(" actions: ")
                for k,v in enumerate(action_space): print(k,v)
                try:
                    act = action_space[int(input(" input [0-10]: " ))]
                except:
                    act = None
            print()
            action_prefix = tokenizer.encode(''.join(['<|act|> '] + [act] + ['<|p1|>'] + [] + ['<|sep|>'] + ['<|start|>']))
            bot_input_ids = to_var([action_prefix + flatten(dialog_hx)]).long()
            
            # generate query conditioned on action
            msg = generate_next(bot_input_ids, top_k=top_k, top_p=top_p, max_length=max_length)
            dialog_hx.append(msg)
            
            # generate bot response
            bot_input_ids = to_var([personas+ flatten(dialog_hx)]).long()
            msg = generate_next(bot_input_ids, top_k=top_k, top_p=top_p, max_length=max_length)
            dialog_hx.append(msg)
    if choice == 2:
        display_dialog_history(dialog_hx)
    return dialog_hx, msg

if __name__=="__main__":
    parser = argparse.ArgumentParser(description='Conversational parameters for interacting with personaGPT.')
    parser.add_argument('-M', '--mode', type=int, 
                        dest='mode', default=1,
                        help='''mode (0 or 1) of interaction: 
                        (0) user gives prompts to persona model,
                        (1) user picks action codes for controlled decoding.''')
    parser.add_argument('-turns', '--num_turns', type=int, 
                        dest='turns', default=8,
                        help='number of turns in conversation (default 8)')
    parser.add_argument('-maxlen', '--max_length', type=int, 
                        dest='max_length', default=1000,
                        help='max num of tokens in convo (default 1000)') 
    parser.add_argument('-k', '--top_k', type=int,
                        dest='top_k', default=10,
                        help='top_k sampling parameter (default 10)')
    parser.add_argument('-p', '--top_p', type=float, 
                        dest='top_p', default=.92,
                        help='nucleus sampling parameter (default 0.92)')    

    args = parser.parse_args()
    personas = get_personas()

    text_input = input(">> User: ")
    print(text_input)
    dialog_hx, msg = interact(args.mode, personas, text_input, length=args.turns, 
             top_k=args.top_k, top_p=args.top_p,
             max_length=args.max_length)
    print(dialog_hx)
    print(tokenizer.decode(msg, skip_special_tokens=True))