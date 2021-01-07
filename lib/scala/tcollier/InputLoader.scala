package tcollier

import scala.io.Source

class InputLoader(filename: String) {
  def getStrings(): Array[String] = {
    val source = Source.fromFile(filename)
    val lines = (for (line <- source.getLines()) yield line).toArray
    source.close()
    lines
  }

  def getInts(): Array[Int] = {
    val source = Source.fromFile(filename)
    val lines = (for (line <- source.getLines()) yield line.toInt).toArray
    source.close()
    lines
  }
}
