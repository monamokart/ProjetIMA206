import streamlit as st
import sys
import numpy as np
import os 

sys.path.append("./")

from scripts.mnist.data_loader import BrainData

import os
from scripts.mnist.evaluate import evaluate_image
from scripts.mnist.inverse import load_inverse


@st.cache
def st_load_data():
    return BrainData().test_data(dataset=True)


@st.cache(allow_output_mutation=True)
def st_load_model(name):
    path = os.path.join(f'output/model-brain-inverse-{name}.pt')
    conf, trainer, hist = load_vxm("brain", path)
    trainer.model.eval()
    return conf, trainer, hist


def double_slider(n1, n2, k):
    col1, col2 = st.beta_columns(2)
    with col1:
        idx1 = st.slider(f'Source data index | id:{k}', 0, n1, 1)
    with col2:
        idx2 = st.slider(f'Target data index | id:{k + 1}', 0, n2, 2)

    return idx1, idx2


def eval_model(model, data, k):
    N_fix, N_mvg = len(data['fix']), len(data['moving'])
    idx1, idx2 = double_slider(N_fix, N_mvg, k)
    val_fix = data['fix'][idx1].unsqueeze(0)
    val_mvt = data['moving'][idx2].unsqueeze(0)
    res = evaluate_image(model, val_fix, val_mvt, mode="inv", show=False)
    col1, col2 = st.beta_columns([5,2])
    with col1:
        st.pyplot(res['fig'])
    with col2:
        st.pyplot(res['flow'])


def app():
    st.write(r"""
    # Inverse-Consistent - Brain Image
    ##  Model for same source distribution 1️⃣ $\rightarrow$ 1️⃣
    ### 🧠 Load model
     """)
    
    pattern = "model-brain-inverse"
    model_availbale = [ filename[len(pattern)+1:-3] for filename in os.listdir('./output') if pattern in filename]
    name = st.selectbox('config:', model_availbale)

    #### Load model
    conf, trainer, hist = st_load_model(name)
    st.write(conf)

    st.write("""### 🧪 Evaluation - Validation set""")
    agree1 = st.checkbox('Display ? id:1', True)
    if agree1:
        data1 = st_load_test_data(conf.fix, conf.moving)
        eval_model(trainer, data1, 0)



if __name__ == '__main__':
    app()
