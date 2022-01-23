################################################################################

# PyChain Ledger

################################################################################

# Imports

import streamlit as st
from dataclasses import dataclass
from typing import Any, List
import datetime as datetime
import pandas as pd
import hashlib

################################################################################

# Set page configuration
st.set_page_config(page_title="PyChain Ledger", page_icon="💸", layout="wide")

################################################################################

# Create a Record Data Class that consists of the `sender`, `receiver`, and `amount` attributes

@dataclass
class Record():
    sender: str
    receiver: str
    amount: float

################################################################################

# Store record data on a Block data class

@dataclass
class Block:
    record: Record
    creator_id: int
    prev_hash: str = "0"
    timestamp: str = datetime.datetime.utcnow().strftime("%H:%M:%S")
    nonce: int = 0

    def hash_block(self):
        sha = hashlib.sha256()

        record = str(self.record).encode()
        sha.update(record)

        creator_id = str(self.creator_id).encode()
        sha.update(creator_id)

        timestamp = str(self.timestamp).encode()
        sha.update(timestamp)

        prev_hash = str(self.prev_hash).encode()
        sha.update(prev_hash)

        nonce = str(self.nonce).encode()
        sha.update(nonce)

        return sha.hexdigest()

# Add Blocks to the Pychain ledger

@dataclass
class PyChain:
    chain: List[Block]
    difficulty: int = 4

    def proof_of_work(self, block):

        calculated_hash = block.hash_block()

        num_of_zeros = "0" * self.difficulty

        while not calculated_hash.startswith(num_of_zeros):

            block.nonce += 1

            calculated_hash = block.hash_block()

        print("Wining Hash", calculated_hash)
        return block

    def add_block(self, candidate_block):
        block = self.proof_of_work(candidate_block)
        self.chain += [block]

    def is_valid(self):
        block_hash = self.chain[0].hash_block()

        for block in self.chain[1:]:
            if block_hash != block.prev_hash:
                print("Blockchain is invalid!")
                return False

            block_hash = block.hash_block()

        print("Blockchain is Valid")
        return True

################################################################################

# Streamlit Code

@st.cache(allow_output_mutation=True)
def setup():
    print("Initializing Chain")
    return PyChain([Block("Genesis", 0)])

st.markdown("# PyChain")
st.markdown("## Store a Transaction Record in the PyChain")

pychain = setup()


# Add Relevant User Inputs to the Streamlit Interface

# Add an input area where you can get a value for `sender`, `recipient`, and `amount` from the user.

input_sender = st.text_input("sender")
input_recipient = st.text_input("recipient")
input_amount = st.text_input("amount")


# Add `Add Block` button

if st.button("Add Block"):
    prev_block = pychain.chain[-1]
    prev_block_hash = prev_block.hash_block()

    # Generate `new_block` so that `Block` consists of an attribute named `record` which is set equal to a `Record` that 
    # contains the `sender`, `receiver`, and `amount` values

    new_block = Block(
        record = Record(input_sender, input_recipient, input_amount),
        creator_id=42,
        prev_hash=prev_block_hash
    )

    pychain.add_block(new_block)
    st.balloons()

st.markdown("## The PyChain Ledger")

pychain_df = pd.DataFrame(pychain.chain).astype(str)
st.write(pychain_df, use_container_width=True)


# Set sidebar

difficulty = st.sidebar.slider("Block Difficulty", 1, 5, 2)
pychain.difficulty = difficulty

st.sidebar.write("# Block Inspector")
selected_block = st.sidebar.selectbox(
    "Which block would you like to see?", pychain.chain
)

st.sidebar.write(selected_block)


# Add validate chain button

if st.button("Validate Chain"):
    st.write(pychain.is_valid())


# Hide Streamlit Style
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

################################################################################

# Test the PyChain Ledger by Storing Records

# In the terminal, run the Streamlit application by using `streamlit run pychain.py`.