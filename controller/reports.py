# @app.route('/generate_report', methods=['GET'])
# def generate_report():

#     email = current_user.email

#     # creating a pdf file to add tables
#     file_name = f"Report-{email}.pdf"
#     my_doc = SimpleDocTemplate(file_name, pagesize = letter)
#     my_obj = []

#     # defining Data to be stored on table

#     my_data = [
#     ["ID", "Expense Amount", "Mode", "Date", "Note"],
#     ]
#     res = get_transactions(email)
#     if res is None:
#         flash("Please add transactions", "error")

#     for i in range(len(res)):
#         temp = [i,res[i]["transaction"],res[i]["mode"],res[i]["datestamp"],res[i]["note"]]
#         my_data.append(temp)

#     # Creating the table with 6 rows
#     row_count = len(res) + 1
#     my_table = Table(my_data, 1 * [1.6 * inch], row_count * [0.5 * inch])
#     # setting up style and alignments of borders and grids
#     my_table.setStyle(
#     TableStyle(
#         [
#             ("ALIGN", (1, 1), (0, 0), "LEFT"),
#             ("VALIGN", (-1, -1), (-1, -1), "TOP"),
#             ("ALIGN", (-1, -1), (-1, -1), "RIGHT"),
#             ("VALIGN", (-1, -1), (-1, -1), "TOP"),
#             ("INNERGRID", (0, 0), (-1, -1), 1, colors.black),
#             ("BOX", (0, 0), (-1, -1), 2, colors.black),
#         ]
#     )
#     )
#     my_obj.append(my_table)
#     my_doc.build(my_obj)
#     path = file_name
#     return send_file(path, as_attachment=True)