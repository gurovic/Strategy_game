import libgame


battle = libgame.get_battle()

battle.send_to(1, "First state!")

print("Second player move:", battle.wait_for(2))
print("Any player move:", battle.wait())

battle.set_points(1, 10)

battle.add_points(2, 20)
battle.add_points(2, -15)

battle.end()
battle.end_due("Test reason")
