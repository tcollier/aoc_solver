package tcollier;

import java.io.BufferedReader;
import java.io.FileReader;
import java.io.FileNotFoundException;
import java.io.IOException;

import java.util.ArrayList;

interface Parser {
  public Object parse(String line);
}

class StringParser implements Parser {
  public Object parse(String line) {
    return line;
  }
}

class IntegerParser implements Parser {
  public Object parse(String line) {
    return new Integer(line);
  }
}

public class InputLoader {
  private String filename;

  public InputLoader(String filename) {
    this.filename = filename;
  }

  public ArrayList<String> getStrings() throws FileNotFoundException, IOException {
    ArrayList<String> values = new ArrayList<String>();
    this.addLinesToList(values, new StringParser());
    return values;
  }

  public ArrayList<Integer> getIntegers() throws FileNotFoundException, IOException {
    ArrayList<Integer> values = new ArrayList<Integer>();
    this.addLinesToList(values, new IntegerParser());
    return values;
  }

  private void addLinesToList(ArrayList values, Parser parser) throws FileNotFoundException, IOException {
    BufferedReader reader = new BufferedReader(new FileReader(filename));
    try {
      String line = reader.readLine();
      while (line != null) {
        values.add(parser.parse(line));
        line = reader.readLine();
      }
    } finally {
      reader.close();
    }
  }
}
