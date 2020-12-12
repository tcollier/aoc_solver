INPUT = open("day8_input.txt", "r").readlines()


def print_part1_ans(input):
    instructions = [l.rstrip() for l in input]
    acc = 0
    curr_ptr = 0
    visited = set()
    while curr_ptr < len(instructions):
        if curr_ptr in visited:
            print(acc)
            break
        visited.add(curr_ptr)
        instruction = instructions[curr_ptr]
        if instruction[0:3] == "acc":
            acc = acc + int(instruction[4:])
            curr_ptr = curr_ptr + 1
        elif instruction[0:3] == "jmp":
            curr_ptr = curr_ptr + int(instruction[4:])
        elif instruction[0:3] == "nop":
            curr_ptr = curr_ptr + 1


def run(instructions):
    acc = 0
    curr_ptr = 0
    visited = set()
    while curr_ptr < len(instructions):
        if curr_ptr in visited:
            raise Exception("Infinite loop detected")
        visited.add(curr_ptr)
        instruction = instructions[curr_ptr]
        if instruction[0:3] == "acc":
            acc = acc + int(instruction[4:])
            curr_ptr = curr_ptr + 1
        elif instruction[0:3] == "jmp":
            curr_ptr = curr_ptr + int(instruction[4:])
        elif instruction[0:3] == "nop":
            curr_ptr = curr_ptr + 1
    return acc


def print_part2_ans(input):
    instructions = [l.rstrip() for l in input]
    for i in range(len(instructions)):
        orig = instructions[i]
        if orig[0:3] == "jmp":
            instructions[i] = f"nop {orig[4:]}"
        elif orig[0:3] == "nop":
            instructions[i] = f"jmp {orig[4:]}"
        else:
            continue

        try:
            print(run(instructions))
        except:
            pass
        instructions[i] = orig


print_part2_ans(INPUT)
