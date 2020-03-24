import benepar
import nltk
nltk.download('punkt')
benepar.download('benepar_en2')


parser = benepar.Parser("benepar_en2")
tree = parser.parse("Short cuts make long delays.")
print(tree)
