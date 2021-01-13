import tcollier.AocExecutor

fun part1Answer(input: List<String>): String {
    return input[0]
}

fun part2Answer(input: List<String>): String {
    return input[1]
}

fun main(args: Array<String>) {
    val input: List<String> = listOf("Hello", "World!")
    val executor = AocExecutor(input, ::part1Answer, ::part2Answer)
    executor.run(args)
}
