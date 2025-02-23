import pandas as pd
import streamlit as st

def modify_tab():
    # Add Tabs Below
    tabs = st.tabs([
        "In House", 
        "Out Source", 
        "Time Converter"
    ])

    int_col = ['UniqueID', 'Sr. No', 'Quantity Required', 'Run Time (min/1000)', 'Cycle Time (seconds)', 'Setup time (seconds)']
    str_col = ['Product Name', 'Components', 'Operation', 'Process Type', 'Machine Number']
    date_col = ['Order Processing Date', 'Promised Delivery Date']

    if "dfm" in st.session_state:
        with tabs[0]:  # In House
            st.session_state.dfm = st.session_state.dfm.reset_index(drop=True)
            rows_added = min(st.session_state.rows_added, len(st.session_state.dfm))
            df_in = st.session_state.dfm.iloc[rows_added:]
            df_in = df_in[df_in['Process Type'] == 'In House']
    
            in_products = df_in['Product Name'].unique()
            in_selected_product = st.selectbox(
                'Select product name:',
                in_products,
                key="in_product"
            )

            in_components = df_in[df_in['Product Name'] == in_selected_product]['Components'].unique()
            in_selected_components = st.selectbox(
                'Select components:',
                in_components,
                key="in_component"
            )
    
            in_field = df_in.columns
            in_selected_fields = st.selectbox(
                'Select fields:',
                in_field,
                key="in_field"
            )
    
            if in_selected_fields in int_col:
                in_edit_input = st.number_input(
                    'Enter new value: ',#(minimum 200)',
                    # min_value=200,
                    step=1,
                    key="in_edit_input"
                )
            elif in_selected_fields in str_col:
                in_edit_input = st.text_input(
                    'Enter new value:',
                    key="in_edit_text"
                )
            else:
                in_edit_input = st.date_input(
                    'Enter new value:',
                    key="in_edit_date"
                )
                
            if st.button('Confirm', key="in_confirm"):
                st.session_state.dfm.loc[
                    (st.session_state.dfm['Product Name'] == in_selected_product) & 
                    (st.session_state.dfm['Components'] == in_selected_components), 
                    in_selected_fields
                ] = in_edit_input

                st.session_state.df.loc[
                    (st.session_state.df['Product Name'] == in_selected_product) & 
                    (st.session_state.df['Components'] == in_selected_components), 
                    in_selected_fields
                ] = in_edit_input
                
                st.success('Data has been successfully changed!')
    
            st.dataframe(st.session_state.dfm[
                (st.session_state.dfm['Product Name'] == in_selected_product) & 
                (st.session_state.dfm['Components'] == in_selected_components)
            ])

            with pd.ExcelWriter('Product Details_v1.xlsx', engine='openpyxl') as writer:
                st.session_state.df.to_excel(writer, sheet_name='P', index=False)
                st.session_state.dfm.to_excel(writer, sheet_name='prodet', index=False)
                # df_pivot.to_excel(writer, sheet_name='Similarity')
                st.session_state.machine_utilization_df.to_excel(writer, sheet_name='Machine Utilisation')
                st.session_state.product_waiting_df.to_excel(writer, sheet_name='Product Waiting Time')
                st.session_state.component_waiting_df.to_excel(writer, sheet_name='Component Waiting Time')
                st.session_state.late_df.to_excel(writer, sheet_name='Late Products')
    
        with tabs[1]:  # Outsource
            df_out = st.session_state.dfm.loc[st.session_state.rows_added:]
            df_out = df_out[st.session_state.dfm['Process Type'] == 'Outsource']
            out_products = df_out['Product Name'].unique()
            out_selected_product = st.selectbox(
                'Select product name:',
                out_products,
                key="out_product"
            )
    
            out_components = df_out[df_out['Product Name'] == out_selected_product]['Components'].unique()
            out_selected_components = st.selectbox(
                'Select components:',
                out_components,
                key="out_component"
            )
    
            out_field = df_out.columns
            out_selected_fields = st.selectbox(
                'Select fields:',
                out_field,
                key="out_field"
            )
            
            if out_selected_fields in int_col:
                out_edit_input = st.number_input(
                    'Enter new value: ',#(minimum 200)',
                    # min_value=200,
                    key="out_edit_input_out"
                )
            elif out_selected_fields in str_col:
                out_edit_input = st.text_input(
                    'Enter new value:',
                    key="out_edit_text_out"
                )
            else:
                out_edit_input = st.date_input(
                    'Enter new value:',
                    step=1,  # Ensures input increments in steps of 1
                    key="out_edit_date_out"
                )
                
            if st.button('Confirm', key="out_confirm"):
                st.session_state.dfm.loc[
                    (st.session_state.dfm['Product Name'] == out_selected_product) & 
                    (st.session_state.dfm['Components'] == out_selected_components), 
                    out_selected_fields
                ] = out_edit_input

                st.session_state.df.loc[
                    (st.session_state.df['Product Name'] == out_selected_product) & 
                    (st.session_state.df['Components'] == out_selected_components), 
                    out_selected_fields
                ] = out_edit_input
                
                st.success('Data has been successfully changed!')
    
            st.dataframe(st.session_state.dfm[
                (st.session_state.dfm['Product Name'] == out_selected_product) & 
                (st.session_state.dfm['Components'] == out_selected_components)
            ])

            with pd.ExcelWriter('Product Details_v1.xlsx', engine='openpyxl') as writer:
                st.session_state.df.to_excel(writer, sheet_name='P', index=False)
                st.session_state.dfm.to_excel(writer, sheet_name='prodet', index=False)
                # df_pivot.to_excel(writer, sheet_name='Similarity')
                st.session_state.machine_utilization_df.to_excel(writer, sheet_name='Machine Utilisation')
                st.session_state.product_waiting_df.to_excel(writer, sheet_name='Product Waiting Time')
                st.session_state.component_waiting_df.to_excel(writer, sheet_name='Component Waiting Time')
                st.session_state.late_df.to_excel(writer, sheet_name='Late Products')
    
        with tabs[2]:  # Time Converter
            # Radio button for conversion options
            conversion_type = st.radio(
                "Choose a conversion type:",
                ("Days to Minutes", "Hours to Minutes", "Minutes to Days"),
                key="conversion_type"
            )
            
            # Input field for the user to provide a value
            input_value = st.number_input(
                "Enter the value to convert:", 
                min_value=0
            )
            
            # Perform conversion based on the selected type
            if conversion_type == "Days to Minutes":
                result = input_value * 24 * 60
                st.write(f"{input_value} days is equivalent to {result} minutes.")
            
            elif conversion_type == "Hours to Minutes":
                result = input_value * 60
                st.write(f"{input_value} hours is equivalent to {result} minutes.")
            
            elif conversion_type == "Minutes to Days":
                result = input_value / (24 * 60)
                st.write(f"{input_value} minutes is equivalent to {result:.6f} days.")