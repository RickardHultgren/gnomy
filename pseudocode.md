# Initialize the game
```
InitializeGame()
    LoadPlayerData()
    SetInitialInventory(keys=10, fruits=5, flowers=5)
    ShowWelcomeMessage()
```

# Main game loop
```
MainGameLoop()
    while GameIsRunning():
        DisplayPlayerStats(keys, fruits, flowers)
        action = GetPlayerInput(["Explore", "Trade", "Check Inventory", "End Game"])
        
        if action == "Explore":
            Explore()
        elif action == "Trade":
            TradeResources()
        elif action == "Check Inventory":
            CheckInventory()
        elif action == "End Game":
            EndGame()
            break
```

# Explore function
Purpose
1. Where is Gnomy? At what tree or path?
2. Who else is there?
3. Explore what options there are.
4. 
```
Explore()
    encounter = RandomEncounter()
    if encounter == "Unlock New Area":
        if keys > 0:
            UpdateInventory(debit="keys", credit="fruits", amount=1)
            UnlockArea()
        else:
            NotifyPlayer("You need more keys to explore!")
    elif encounter == "Help NPC":
        if fruits > 0:
            UpdateInventory(debit="fruits", credit="flowers", amount=1)
            StrengthenBondWithNPC()
        else:
            NotifyPlayer("You need more fruits to assist!")
    elif encounter == "Gain Skill":
        UpdateInventory(debit="keys", credit="fruits", amount=2)
        GainSkill()
```

# Trade function
```
TradeResources()
    tradeOption = GetPlayerInput(["Keys ↔ Fruits", "Flowers ↔ Keys", "Fruits ↔ Flowers"])
    if tradeOption == "Keys ↔ Fruits":
        if keys >= 1:
            UpdateInventory(debit="keys", credit="fruits", amount=1)
        else:
            NotifyPlayer("Not enough keys!")
    elif tradeOption == "Flowers ↔ Keys":
        if flowers >= 1:
            UpdateInventory(debit="flowers", credit="keys", amount=1)
        else:
            NotifyPlayer("Not enough flowers!")
    elif tradeOption == "Fruits ↔ Flowers":
        if fruits >= 1:
            UpdateInventory(debit="fruits", credit="flowers", amount=1)
        else:
            NotifyPlayer("Not enough fruits!")
```

# Inventory check
```
CheckInventory()
    ShowInventoryDetails(keys, fruits, flowers)
```

# Update inventory using double-entry bookkeeping
```
UpdateInventory(debit, credit, amount)
    if debit == "keys":
        keys -= amount
    elif debit == "fruits":
        fruits -= amount
    elif debit == "flowers":
        flowers -= amount
    
    if credit == "keys":
        keys += amount
    elif credit == "fruits":
        fruits += amount
    elif credit == "flowers":
        flowers += amount

    LogTransaction(debit, credit, amount)
```

# End the game
```
EndGame()
    SavePlayerData()
    ShowGoodbyeMessage()
```