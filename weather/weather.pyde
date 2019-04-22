title_font = PFont()
label_font = PFont()
legend_font = PFont()
top_margin = 345
left_margin = 360

months = ["JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"]
num_days = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
data_attrs = []
date_idx = 0 
tmin_idx = 0 # min temp
tmax_idx = 0 # max temp
tavg_idx = 0 # avg temp
prcp_idx = 0 # precip amt
awnd_idx = 0 # avg wind speed
wt01_idx = 0 # -/1 fog
curr_row = 1 # iteration of curr_row assumes rows sorted by date

def setup():
    size(3508, 4961)
    background(255)
    
    # Get data
    data_attrs = loadStrings("data/2018.csv")[0].replace("\"", "").split(",")
    data_table = loadTable("data/2018.csv")
    global date_idx, tmin_idx, tmax_idx, tavg_idx, prcp_idx, awnd_idx, wt01_idx
    date_idx = data_attrs.index("DATE")
    tmin_idx = data_attrs.index("TMIN")
    tmax_idx = data_attrs.index("TMAX")
    tavg_idx = data_attrs.index("TAVG")
    prcp_idx = data_attrs.index("PRCP")
    awnd_idx = data_attrs.index("AWND")
    wt01_idx = data_attrs.index("WT01")
    
    # Draw title
    textAlign(CENTER)
    title_font = createFont("Futura-Medium", 60)
    textFont(title_font)
    fill(0)
    text("SEATTLE-TACOMA INT'L AIRPORT STATION, 2018", width/2, height-575)
    
    # Draw cells
    draw_all(3, 4, 200, data_table)
    
    # Draw legend
    l_prcp = 0.13
    l_tavg = 41.0
    l_tmax = 47.0
    l_tmin = 35.0
    l_wt01 = 1.0
    l_start_angle = -(TWO_PI / 30)
    l_end_angle = 0
    
    textAlign(LEFT)
    legend_font = createFont("Futura-Medium", 32)
    textFont(legend_font)
    noStroke()
    
    color_list = [[0, 120, 255, 150], [190, 0, 255, 120], [255, 80, 0, 150], 
                  [100, 220, 200, 255], [190, 160, 255, 180], [250, 250, 250, 255]]
    attr_list = ["MIN. TEMPERATURE", "AVG. TEMPERATURE", "MAX. TEMPERATURE", 
                 "PRECIPITATION", "WIND SPEED", "PRESENCE OF FOG"]
    curr_pos = 1075
    l_space = 500
    for i in range(3):
        fill(color_list[i][0], color_list[i][1], color_list[i][2], color_list[i][3])
        ellipse(curr_pos, height - 450, 50, 50)
        fill(0)
        noStroke()
        text(attr_list[i], curr_pos + 50, height - 440)
        curr_pos += l_space
    curr_pos = 1075
    for i in range(3, len(attr_list)):
        fill(color_list[i][0], color_list[i][1], color_list[i][2], color_list[i][3])
        if attr_list[i] == "PRESENCE OF FOG":
            stroke(100, 100, 100, 255)
            strokeWeight(2)
            
            # special case
            
            # fill(0)
            # noStroke()
            # text(attr_list[i], curr_pos + 50, height - 350)
            # curr_pos += l_space
            # continue
        
        ellipse(curr_pos, height - 360, 50, 50)
        fill(0)
        noStroke()
        text(attr_list[i], curr_pos + 50, height - 350)
        curr_pos += l_space

    # day outline
    # noFill()
    # stroke(0, 0, 0, 255)
    # strokeWeight(5)
    # arc(width / 2 - 100, height - 200, 800, 800, l_start_angle, l_end_angle, PIE)
    
    # Save
    save("weather.png")


def draw_all(c, r, pad, data_table):
    global curr_row
    diam = 800
    month_num = 0
    for j in range(r):
        for i in range(c):
            x = left_margin + (diam / 2) + (i * (diam + pad))
            y = top_margin + (diam / 2) + (j * (diam + pad))
            
            draw_temp(x, y, diam, month_num, data_table)
            curr_row -= num_days[month_num]
            draw_wind(x, y, diam, month_num, data_table)
            curr_row -= num_days[month_num]
            draw_prcp(x, y, diam, month_num, data_table)
            curr_row -= num_days[month_num]
            draw_fog(x, y, diam, month_num, data_table)
            
            draw_label(x, y, diam, months[month_num])
            month_num += 1


def draw_label(centerX, centerY, diam, month_text):
    textAlign(CENTER)
    label_font = createFont("Futura-Medium", 32)
    textFont(label_font)
    fill(0)
    text(month_text, centerX, centerY + (diam / 2) + 50)


def change_range(min1, max1, min2, max2, val):
    range1 = max1 - min1
    range2 = max2 - min2
    return (((val - min1) * range2) / range1) + min2


def draw_temp(centerX, centerY, diam, month_num, data_table):
    global curr_row
    ellipseMode(CENTER)
    
    days = num_days[month_num]
    angle_step = TWO_PI / days
    for i in range(days):
        start_angle = (i * angle_step) - HALF_PI
        end_angle = (i * angle_step) + angle_step - HALF_PI
        tmin = data_table.getFloat(curr_row, tmin_idx)
        tmax = data_table.getFloat(curr_row, tmax_idx)
        tavg = data_table.getFloat(curr_row, tavg_idx)
        prcp = data_table.getFloat(curr_row, prcp_idx)
        
        strokeCap(ROUND)
        noFill()
         
        # Draw tmax indicator
        weight = change_range(25, 100, 30, 90, tmax)
        # weight = 50
        strokeWeight(weight)
        stroke(255, 80, 0, 100)
        max_diam = change_range(25, 100, 0, diam - 200, tmax)
        arc(centerX, centerY, max_diam, max_diam, start_angle, end_angle)
        
        # Draw tmin indicator
        weight = change_range(25, 100, 30, 90, tmin)
        # weight = 50
        strokeWeight(weight)
        stroke(0, 120, 255, 90)
        min_diam = change_range(25, 100, 0, diam - 200, tmin)
        arc(centerX, centerY, min_diam, min_diam, start_angle, end_angle)
        
        # Draw tavg indicator
        weight = change_range(25, 100, 30, 90, tavg)
        # weight = 50
        strokeWeight(weight)
        stroke(190, 0, 255, 80)
        avg_diam = change_range(25, 100, 0, diam - 200, tavg)
        arc(centerX, centerY, avg_diam, avg_diam, start_angle, end_angle)
        
        # Precip indicator (green)
        dot_space = 0.1
        dot_len = 0.001
        stroke(100, 220, 200, 255)
        dot_size = 0
        if prcp > 0 and prcp <= 0.1:
            dot_size = 10
        elif prcp > 0.1 and prcp <= 0.4:
            dot_size = 20
        elif prcp > 0.4 and prcp <= 1.2:
            dot_size = 35
        elif prcp > 1.2:
            dot_size = 50
        
        curr_start = start_angle
        strokeWeight(dot_size)
        arc(centerX, centerY, max_diam + 200, max_diam + 200, curr_start + angle_step / 2, curr_start + angle_step / 2 + 0.001)
            
        curr_row += 1
            
            
def draw_wind(centerX, centerY, diam, month_num, data_table):
    global curr_row
    ellipseMode(CENTER)
    
    days = num_days[month_num]
    angle_step = TWO_PI / days
    for i in range(days):
        start_angle = (i * angle_step) - HALF_PI
        end_angle = (i * angle_step) + angle_step - HALF_PI
        awnd = data_table.getFloat(curr_row, awnd_idx)
        
        noFill()

        # Draw wind speed indicator
        wind_diam = change_range(5, 20, diam - 300, diam + 150, awnd)
        stroke(255, 255, 255, 200)
        strokeWeight(15)
        strokeCap(ROUND)
        arc(centerX, centerY, wind_diam, wind_diam, start_angle, start_angle + 0.02 * awnd)
        
        stroke(190, 160, 255, 180)
        strokeWeight(10)
        # strokeCap(SQUARE)
        arc(centerX, centerY, wind_diam, wind_diam, start_angle, start_angle + 0.02 * awnd)
        
        curr_row += 1


def draw_prcp(centerX, centerY, diam, month_num, data_table):
    global curr_row
    ellipseMode(CENTER)
    
    days = num_days[month_num]
    angle_step = TWO_PI / days
    for i in range(days):
        start_angle = (i * angle_step) - HALF_PI
        end_angle = (i * angle_step) + angle_step - HALF_PI
        tmax = data_table.getFloat(curr_row, tmax_idx)
        max_diam = change_range(25, 100, 0, diam - 200, tmax)
        prcp = data_table.getFloat(curr_row, prcp_idx)
                
        strokeCap(ROUND)
        noFill()
        
        # Precip indicator (green)
        dot_space = 0.1
        dot_len = 0.001
        stroke(100, 220, 200, 100)
        dot_size = 0
        if prcp > 0 and prcp <= 0.1:
            dot_size = 15
        elif prcp > 0.1 and prcp <= 0.4:
            dot_size = 30
        elif prcp > 0.4 and prcp <= 1.2:
            dot_size = 40
        elif prcp > 1.2:
            dot_size = 60
        
        curr_start = start_angle
        strokeWeight(dot_size)
        arc(centerX, centerY, max_diam + 200, max_diam + 200, curr_start + angle_step / 2, curr_start + angle_step / 2 + 0.001)
            
        curr_row += 1


def draw_fog(centerX, centerY, diam, month_num, data_table):
    global curr_row
    ellipseMode(CENTER)
    
    days = num_days[month_num]
    angle_step = TWO_PI / days
    for i in range(days):
        start_angle = (i * angle_step) - HALF_PI
        end_angle = (i * angle_step) + angle_step - HALF_PI
        tavg = data_table.getFloat(curr_row, tavg_idx)
        avg_diam = change_range(25, 100, 0, diam - 200, tavg)
        wt01 = data_table.getFloat(curr_row, wt01_idx)
        
        noStroke()
        fill(255, 255, 255, 200)
         
        # Draw fog indicator
        if wt01 == 1.0:
            arc(centerX, centerY, avg_diam, avg_diam, start_angle + 0.07, end_angle - 0.07)

        curr_row += 1
