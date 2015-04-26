import win32com.client
from datetime import date

o = win32com.client.Dispatch('Outlook.Application')
#app = o.CreateItem('AppointmentItem')
app = o.CreateItem(1)
app.Subject = 'Test App'
app.Start = '26/04/2015'
app.End = '27/04/2015'
app.Save()
