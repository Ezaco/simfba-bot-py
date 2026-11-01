def GetPriorityFields(data):
    attrList = []
    if data['Position'] == "QB":
        sgr = ""
        if data['Shotgun'] == -1:
            sgr = "Under Center"
        elif data['Shotgun'] == 0:
            sgr = "Balanced"
        else:
            sgr = "Shotgun"
        attrList = [
        {
          "name": "Agility",
          "value": data['AgilityGrade'],
          "inline": True,
        },
        {
          "name": "Speed",
          "value": data['SpeedGrade'],
          "inline": True,
        },
        {
          "name": "Carrying",
          "value": data['CarryingGrade'],
          "inline": True,
        },
        {
          "name": "Strength",
          "value": data['StrengthGrade'],
          "inline": True,
        },
        {
          "name": "Throw Power",
          "value": data['ThrowPowerGrade'],
          "inline": True,
        },
        {
          "name": "Throw Accuracy",
          "value": data['ThrowAccuracyGrade'],
          "inline": True, 
        },
        {
          "name": "Shotgun Rating",
          "value": sgr,
          "inline": True, 
        }
        ]
    elif data['Position'] == "RB":
         attrList = [
              {
          "name": "Agility",
          "value": data['AgilityGrade'],
          "inline": True,
        },
        {
          "name": "Speed",
          "value": data['SpeedGrade'],
          "inline": True,
        },
        {
          "name": "Carrying",
          "value": data['CarryingGrade'],
          "inline": True,
        },   {
          "name": "Catching",
          "value": data['CatchingGrade'],
          "inline": True,
        },
        {
          "name": "Pass Block",
          "value": data['PassBlockGrade'],
          "inline": True,
        },
        {
          "name": "Strength",
          "value": data['StrengthGrade'],
          "inline": True,
        }
        ]
    elif data['Position'] == "FB":
        attrList = [
              {
          "name": "Agility",
          "value": data['AgilityGrade'],
          "inline": True,
        },
        {
          "name": "Speed",
          "value": data['SpeedGrade'],
          "inline": True,
        },
        {
          "name": "Carrying",
          "value": data['CarryingGrade'],
          "inline": True,
        },   {
          "name": "Catching",
          "value": data['CatchingGrade'],
          "inline": True,
        },
        {
          "name": "Pass Block",
          "value": data['PassBlockGrade'],
          "inline": True,
        },{
          "name": "Run Block",
          "value": data['RunBlockGrade'],
          "inline": True,
        },
        {
          "name": "Strength",
          "value": data['StrengthGrade'],
          "inline": True,
        }
        ]
    elif data['Position'] == "WR":
        attrList = [
              {
          "name": "Agility",
          "value": data['AgilityGrade'],
          "inline": True,
        },
        {
          "name": "Speed",
          "value": data['SpeedGrade'],
          "inline": True,
        },
        {
          "name": "Carrying",
          "value": data['CarryingGrade'],
          "inline": True,
        },   {
          "name": "Catching",
          "value": data['CatchingGrade'],
          "inline": True,
        },
        {
          "name": "Route Running",
          "value": data['RouteRunningGrade'],
          "inline": True,
        },
        {
          "name": "Strength",
          "value": data['StrengthGrade'],
          "inline": True,
        }
        ]
    elif data['Position'] == "TE":
        attrList = [
              {
          "name": "Agility",
          "value": data['AgilityGrade'],
          "inline": True,
        },
        {
          "name": "Speed",
          "value": data['SpeedGrade'],
          "inline": True,
        },
        {
          "name": "Carrying",
          "value": data['CarryingGrade'],
          "inline": True,
        },   
        {
          "name": "Catching",
          "value": data['CatchingGrade'],
          "inline": True,
        },
        {
          "name": "Route Running",
          "value": data['RouteRunningGrade'],
          "inline": True,
        },
        {
          "name": "Strength",
          "value": data['StrengthGrade'],
          "inline": True,
        },        
        {
          "name": "Pass Block",
          "value": data['PassBlockGrade'],
          "inline": True,
        },
        {
          "name": "Run Block",
          "value": data['RunBlockGrade'],
          "inline": True,
        },
        ]
    elif data['Position'] == "OG" or data['Position'] == "OT" or data['Position'] == "C":
        attrList = [
              {
          "name": "Agility",
          "value": data['AgilityGrade'],
          "inline": True,
        },
        {
          "name": "Strength",
          "value": data['StrengthGrade'],
          "inline": True,
        },        
        {
          "name": "Pass Block",
          "value": data['PassBlockGrade'],
          "inline": True,
        },
        {
          "name": "Run Block",
          "value": data['RunBlockGrade'],
          "inline": True,
        },
        ]
    elif data['Position'] == "DE":
        attrList = [
              {
          "name": "Agility",
          "value": data['AgilityGrade'],
          "inline": True,
        },
        {
          "name": "Speed",
          "value": data['SpeedGrade'],
          "inline": True,
        },
        {
          "name": "Tackle",
          "value": data['TackleGrade'],
          "inline": True,
        },
        {
          "name": "Strength",
          "value": data['StrengthGrade'],
          "inline": True,
        },        
        {
          "name": "Pass Rush",
          "value": data['PassRushGrade'],
          "inline": True,
        },
        {
          "name": "Run Defense",
          "value": data['RunDefenseGrade'],
          "inline": True,
        },
        ]
    elif data['Position'] == "DT":
        attrList = [
              {
          "name": "Agility",
          "value": data['AgilityGrade'],
          "inline": True,
        },
        {
          "name": "Tackle",
          "value": data['TackleGrade'],
          "inline": True,
        },
        {
          "name": "Strength",
          "value": data['StrengthGrade'],
          "inline": True,
        },        
        {
          "name": "Pass Rush",
          "value": data['PassRushGrade'],
          "inline": True,
        },
        {
          "name": "Run Defense",
          "value": data['RunDefenseGrade'],
          "inline": True,
        },
        ]
    elif data['Position'] == "ILB" or data['Position'] == "OLB":
        attrList = [
              {
          "name": "Agility",
          "value": data['AgilityGrade'],
          "inline": True,
        },
        {
          "name": "Speed",
          "value": data['SpeedGrade'],
          "inline": True,
        },
        {
          "name": "Tackle",
          "value": data['TackleGrade'],
          "inline": True,
        },
        {
          "name": "Strength",
          "value": data['StrengthGrade'],
          "inline": True,
        },        
        {
          "name": "Pass Rush",
          "value": data['PassRushGrade'],
          "inline": True,
        },
        {
          "name": "Run Defense",
          "value": data['RunDefenseGrade'],
          "inline": True,
        },
        {
          "name": "Zone Coverage",
          "value": data['ZoneCoverageGrade'],
          "inline": True,
        },
        {
          "name": "Man Coverage",
          "value": data['ManCoverageGrade'],
          "inline": True,
        },
        ]
    elif data['Position'] == "CB":
        attrList = [
              {
          "name": "Agility",
          "value": data['AgilityGrade'],
          "inline": True,
        },
        {
          "name": "Speed",
          "value": data['SpeedGrade'],
          "inline": True,
        },
        {
          "name": "Tackle",
          "value": data['TackleGrade'],
          "inline": True,
        },
        {
          "name": "Strength",
          "value": data['StrengthGrade'],
          "inline": True,
        },        
        {
          "name": "Zone Coverage",
          "value": data['ZoneCoverageGrade'],
          "inline": True,
        },
        {
          "name": "Man Coverage",
          "value": data['ManCoverageGrade'],
          "inline": True,
        },
        {
          "name": "Catching",
          "value": data['CatchingGrade'],
          "inline": True,
        }
        ]
    elif data['Position'] == "FS" or data['Position'] == "SS":
        attrList = [
              {
          "name": "Agility",
          "value": data['AgilityGrade'],
          "inline": True,
        },
        {
          "name": "Speed",
          "value": data['SpeedGrade'],
          "inline": True,
        },
        {
          "name": "Tackle",
          "value": data['TackleGrade'],
          "inline": True,
        },
        {
          "name": "Strength",
          "value": data['StrengthGrade'],
          "inline": True,
        },
        {
          "name": "Run Defense",
          "value": data['RunDefenseGrade'],
          "inline": True,
        },       
        {
          "name": "Zone Coverage",
          "value": data['ZoneCoverageGrade'],
          "inline": True,
        },
        {
          "name": "Man Coverage",
          "value": data['ManCoverageGrade'],
          "inline": True,
        },
        {
          "name": "Catching",
          "value": data['CatchingGrade'],
          "inline": True,
        }
        ]
    elif data['Position'] == "K":
        attrList = [
        {
          "name": "Kick Power",
          "value": data['KickPowerGrade'],
          "inline": True,
        },
        {
          "name": "Kick Accuracy",
          "value": data['KickAccuracyGrade'],
          "inline": True,
        }
        ]
    elif data['Position'] == "P":
        attrList = [
         {
          "name": "Punt Power",
          "value": data['PuntPowerGrade'],
          "inline": True,
        },
        {
          "name": "Punt Accuracy",
          "value": data['PuntAccuracyGrade'],
          "inline": True,
        }
        ]
    attrList.insert(0, {
          "name": "Stars",
          "value": data['Stars'],
          "inline": False,
        })
    attrList.insert(0, {
          "name": "Overall",
          "value": data['OverallGrade'],
          "inline": True,
        })
    attrList.append({
          "name": "Football IQ",
          "value": data['FootballIQGrade'],
          "inline": True,
        })
    attrList.append({
          "name": "Stamina",
          "value": data['StaminaGrade'],
          "inline": True,
        })
    attrList.append({
          "name": "Potential",
          "value": data['PotentialGrade'],
          "inline": True,
        })
    attrList.append({
          "name": "Injury",
          "value": data['InjuryGrade'],
          "inline": True,
        })
    if len(data['RedshirtStatus']) > 0:
        attrList.append({
          "name": "Redshirt Status",
          "value": data['RedshirtStatus'],
          "inline": True,
        })
    return attrList


LAX_ATTRIBUTES = {
    "Attack": [("Speed", "speed"), ("Shot Power", "shotPower"), ("Shot Accuracy", "shotAccuracy"), ("Passing", "passing"), ("Handling", "handling"), ("Lax IQ", "laxiq")],
    "Midfield": [("Speed", "speed"), ("Shot Power", "shotPower"), ("Shot Accuracy", "shotAccuracy"), ("Passing", "passing"), ("Handling", "handling"), ("Stick Check", "stickCheck"), ("Body Check", "bodyCheck"), ("Lax IQ", "laxiq")],
    "Defense": [("Speed", "speed"), ("Body Check", "bodyCheck"), ("Stick Check", "stickCheck"), ("Handling", "handling"), ("Passing", "passing"), ("Lax IQ", "laxiq")],
    "Goalie": [("Goalie Blocking", "goalieBlocking"), ("Goalie Vision", "goalieVision"), ("Passing", "passing"), ("Lax IQ", "laxiq")],
    "FOGO": [("Faceoff", "faceoff"), ("Speed", "speed"), ("Body Check", "bodyCheck"), ("Stick Check", "stickCheck"), ("Handling", "handling"), ("Lax IQ", "laxiq")],
}

def GetLaxPriorityFields(player):
    grades = player["grades"]
    position = player["position"]
    if position == "FOGO" or player["archetype"].upper() == "FOGO":
        position = "FOGO"
    attributes = LAX_ATTRIBUTES.get(position, LAX_ATTRIBUTES["Midfield"])
    attrList = [
        {"name": "Overall", "value": grades["overall"], "inline": True},
        {"name": "Potential", "value": grades["potential"], "inline": True},
        {"name": "​", "value": "​", "inline": True},
    ]
    for name, key in attributes:
        attrList.append({"name": name, "value": grades[key], "inline": True})
    injury = player["injury"]
    if injury["isInjured"]:
        details = injury["name"] or injury["injuryType"] or "Injured"
        if injury["recoveryWeeks"]:
            details += f" ({injury['recoveryWeeks']} weeks)"
        attrList.append({"name": "Injury", "value": details, "inline": False})
    return attrList
