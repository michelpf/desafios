# Formatação de textos

## Introdução

Para os desafios parte 1 e parte 2 foi criado uma função *truncate* que recebe 
como parâmetro de entrada um texto, `text` para justificar, um tamanho, `max_char_line` 
de justificação e, por fim, um parâmetro opcional booleano para ativar a justificação por 
espaços em branco entre as palavras, `justification`.

Foi implementado um controle simples de *try* *catch* para teste e captura de exceções em 
tempo de execução.

Para fins de controle e evitar situações que o algoritmo não funcione adequadamente, foi 
incluído um valor mínimo para truncar no valor de 15. Se for solicitado truncar um texto 
com tamanho menor 15 será lançada uma *Exception* com mensagem informado que foi excedido o
valor mínimo.

## Modo de uso

O script foi desenvolvido para ser executado em uma IDE como o PyCharm diretamente pelo 
arquivo **string_justify.py**.

Para testar novos valores, edite o trecho de código abaixo.

```python
text = 'In the beginning God created the heavens and the earth. Now the earth was ' \
       'formless and empty, darkness was over the surface of the deep, and the Spirit ' \
       'of God was hovering over the waters.\nAnd God said, "Let there be light," and there was light. ' \
       'God saw that the light was good, and he separated the light from the darkness. God called the ' \
       'light "day," and the darkness he called "night." And there was evening, and there was morning - the first day.'
text_justified = truncate(text, 40)
text_justified_spaces = truncate(text, 40, justification=True)
```
As demais instruções imprimirão em tela os resultados.