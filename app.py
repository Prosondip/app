import sys
from jinja2 import Template
import matplotlib.pyplot as plt

def student_details(lines,id):
  found=False
  for line in lines:
    data=line.split(',')
    if data[0]==id:
      found=True
      break
  if found==False:
    return wrong_input()
    
  html_data= """<!DOCTYPE html>
  <head><title>Student Data</title>
  table, th, td {
  border: 1px solid black;
  }
  </head>
  <body>
    <h1>Student Details</h1>
    <table>
      <tr>
        <th>Student id</th>
        <th>Course id</th>
        <th>Marks></th>
      </tr>
      {% set sum=namespace(value=0) %}
      {% for line in lines %}
      {% set data=line.split(',') %}
      {% if data[0]==id %}
      {% set sum.value=sum.value+data[2] | int %}
          <tr>
            <td>{{ data[0] }}</td>
            <td>{{ data[1] }}</td>
            <td>{{ data[2] }}</td>
          </tr>
      {% endif %}
      {% endfor %}
      <tr>
        <td colspan="2">Total Marks</td>
          <td>{{ sum.value }}</td>
      </tr>
    </table>
  </body></html>"""
  template=Template(html_data)
  template_output=template.render(lines=lines,id=id)
  return template_output
  
def course_details(lines, id):
  found=False
  for line in lines:
    data=line.split(',')
    if data[1]==id:
      found=True
      break
  if found==False:
    return wrong_input()
    
  list_data=[]
  for line in lines:
    data=line.split(',')
    if data[1]==id:
      list_data.append(data[2])
  fig, axe = plt.subplots(dpi=800)
  plt.xlabel("Marks")
  plt.ylabel("Frequency")
  axe.hist(list_data)
  fig.savefig("img.png")
  plt.close(fig)
  html_data = """<!DOCTYPE html>
  <head><title>Course Data</title>
  table, th, td {
  border: 1px solid black;
  }
  </head>
  <body>
    <h1>Course Details</h1>
    <table>
      <tr>
        <td>Average Marks</td>
        <td>Maximum Marks</td>
      </tr>
      {% set max=namespace(value=0) %}
      {% set count=namespace(value=0) %}
      {% set total=namespace(value=0) %}
      {% for line in lines %}
        {% set data=line.split(',') %}
        {% if data[1]==id %}
          {% set count.value=count.value+1 %}
          {% set data_2=data[2] | int %}
          {% set total.value=total.value+data_2 %}
          {% if data_2 > max.value %}
            {% set max.value=data_2 %}
          {% endif %}
        {% endif %}
      {% endfor %}
      {% set avg=total.value/count.value %}
      <tr>
        <td>{{ avg }}</td>
        <td>{{ max.value }}</td>
      </tr>
    </table>
    <img src="img.png">
  </body></html>"""
 
  template=Template(html_data)
  template_output=template.render(lines=lines,id=id)
  return template_output
  
def wrong_input():
  return """<!DOCTYPE html>
  <head><title>Something Went Wrong</title></head>
  <body>
    <h1>Wrong Inputs</h1>
    <p>Something went wrong</p>
  </body>
  </html>"""
# main program starts from here
first_param=sys.argv[1]
second_param=sys.argv[2]
output=""
if first_param!="-s" and first_param!="-c":
  output=wrong_input()
else:
  data_file=open("data.csv","r")
  #skip first line of the file as it is header
  data_file.readline()
  lines=data_file.readlines()
  data_file.close()
  if first_param=="-s":
    output=student_details(lines,second_param)
  else:
    output=course_details(lines,second_param)

output_file=open("output.html","w")
output_file.write(output)
output_file.close()
