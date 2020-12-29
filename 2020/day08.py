INPUT = [l.rstrip() for l in open("day08_input.txt", "r").readlines()]


def run(instructions, fail_on_loop):
    acc = 0
    curr_ptr = 0
    visited = set()
    while curr_ptr < len(instructions):
        if curr_ptr in visited:
            if fail_on_loop:
                raise Exception("Infinite loop detected")
            else:
                return acc
        visited.add(curr_ptr)
        instruction = instructions[curr_ptr]
        if instruction[0:3] == "acc":
            acc += int(instruction[4:])
            curr_ptr += 1
        elif instruction[0:3] == "jmp":
            curr_ptr += int(instruction[4:])
        elif instruction[0:3] == "nop":
            curr_ptr += 1
    return acc


def print_part1_ans(input):
    print(run(input, False))


def print_part2_ans(input):
    for i in range(len(input)):
        orig = input[i]
        if orig[0:3] == "jmp":
            input[i] = f"nop {orig[4:]}"
        elif orig[0:3] == "nop":
            input[i] = f"jmp {orig[4:]}"
        else:
            continue

        try:
            print(run(input, True))
            break
        except:
            pass
        input[i] = orig


print_part2_ans(INPUT)
