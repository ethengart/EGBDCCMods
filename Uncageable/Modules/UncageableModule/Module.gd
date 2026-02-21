extends Module

func _init():
	id = "UncageableModule"
	author = "EthenGart"

func onEquippedItemsChange():
	# GM.pc.getInventory().removeEquippedItemsWithTag(ItemTag.ChastityCage)
	for item in GM.pc.getInventory().getEquippedItemsWithTag(ItemTag.BDSMRestraint):
		if(item.getClothingSlot() == InventorySlot.Penis):
			GM.pc.getInventory().removeEquippedItem(item)

func registerEventTriggers():
	# This is probably misuse of this call, but most other events didn't work
	# (needs to catch the player changing through loads / signals being received too early)
	if(GM.pc != null && is_instance_valid(GM.pc)):
		if(!GM.pc.getInventory().is_connected("equipped_items_changed", self, "onEquippedItemsChange")):
			GM.pc.getInventory().connect("equipped_items_changed", self, "onEquippedItemsChange")
			#Log.printerr("UncageableModule attached event to player")
	# else:
		# Log.printerr("UncageableModule unable to attach signal, maybe another load is coming?")
