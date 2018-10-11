def get_arguments(info):
	arguments = info.operation.selection_set.selections[0].arguments
	argument_dict = {}

	if arguments:		
		for argument in arguments:
			argument_dict[argument.name.value] = argument.value.value
	
	return argument_dict