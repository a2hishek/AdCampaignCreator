import streamlit as st
from llm import ad_chain, image_llm

#function to invoke the llms

def generate():

    response = ad_chain.invoke(
        {
            "brand_name": brand_name,
            "product_name": product_name,
            "brand_description": brand_description,
            "age_category": age_category,
            "gender": gender,
            "campaign_goal": campaign_goal,
            "tone": tone,
        }
    )

    #store the response in session state for later access
    st.session_state.generated_response = response

    #image generation setup
    message = {
    "role": "user",
    "content": response.image_prompt,
    }

    response = image_llm.invoke(
        [message],
        generation_config=dict(response_modalities=["TEXT", "IMAGE"]),
    )

    #obtain image in base64 format from the llm response 
    image_base64 = response.content[1].get("image_url").get("url").split(",")[-1]

    #store the image string in session state
    st.session_state.image_base64 = image_base64

    
#UI Set-Up 
st.set_page_config(layout="wide")

st.header("AI Ad Campaign Generator")
st.divider()
# create two columns for user input and llm output
left_col, right_col = st.columns([0.55,0.45],border=True)

# user input column
with left_col:
    st.subheader("Campaign Summary:", divider="gray")
    # create a form for user input with llm invocation button
    with st.form("Campaign Summary"):
        left_con, right_con = st.columns(2)

        brand_name = left_con.text_input("Brand Name:", placeholder="Enter your brand name")
        product_name = right_con.text_input("Product Name:", placeholder="Enter your product name")

        age_category = left_con.selectbox("Age Category:",('Kids','Teens','Adults', 'Old'),index=None)
        gender = right_con.selectbox("Gender:",('Male', 'Female', 'Other'),index=None)
        campaign_goal = left_con.selectbox("Objective:",('Awareness','Conversions','Store Visits'),index=None)
        tone = right_con.selectbox("Style:",('Professional','Witty','Sarcasm'),index=None)
        brand_description = st.text_area("Description:", placeholder="Tell about your brand and product")


        st.form_submit_button("Generate Campaign", on_click=generate)


# llm output column
with right_col:
    st.subheader("Generated Campaign", divider="gray")

    if "generated_response" in st.session_state:
        response = st.session_state.generated_response

        if "image_base64" in st.session_state:
            img_data = st.session_state.image_base64
 
            img_html = f"""
                <div style="display: flex; justify-content: center; align-items: center;">
                <img src="data:image/png;base64,{img_data}" style="width: 300px; height: 240px"/>
                </div>
                """
            st.markdown("---")
            st.markdown("<h1 style='text-align: center; font-size: 30px; color: #2E8B57;'>{}</h1>".format(response.headline), unsafe_allow_html=True)
            st.markdown(img_html, unsafe_allow_html=True)
            st.markdown(f"<p style='font-size: 15px;'>{response.description}</p>", unsafe_allow_html=True)
            st.markdown(f"<p style='text-align: center, font-size: 20px; font-weight: bold; color: #D2691E;'>{response.call_to_action}</p>", unsafe_allow_html=True)
            st.markdown("---")







