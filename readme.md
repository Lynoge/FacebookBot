Optimist Prime Facebook Messenger Bot
======

Optimist Prime é um Bot Messenger do Facebook que suporta reconhecimento de voz, processamento de linguagem natural e recursos como: pesquisar restaurantes nas proximidades, pesquisar notícias de tendências, transcrever e salvar memorandos na nuvem. Ele também salva dados do usuário (com permissões, é claro), como locais favoritos, pode fornecer saudações personalizadas (reconhecimento do horário do usuário em qualquer fuso horário, ou seja, bom dia / boa noite) e respostas divertidas, etc.

(Para uma implementação de prova de conceito "echo bot" mais simples do Facebook Messenger Bot, confira [este projeto simplificado](https://github.com/hungtraan/FacebookBot-echobot-simple) com [10 minutos de tutorial](https://cli.traan.vn/how-to-create-a-facebook-bot-in-10-minutes-the-complete-tutorial-from-zero-to-hero-ku-352dca274046))

**Índice**


- [Características](#features)
- [Screenshots](#screenshots)
- [Uso](#usage)
  - [Dependências, banco de dados e chaves de API](#dependencies-database-and-api-keys)
  - [Implantando na nuvem](#deploying-to-the-cloud)
  - [Reconhecimento de voz](#voice-recognition)
  - [Processamento de linguagem natural](#natural-language-processing)
  - [Recursos personalizados](#custom-features)
    - [1. Pesquisa de negócios / restaurantes](#1-businessrestaurant-search)
    - [2. Pesquisa de notícias em alta](#2-trending-news-search)
    - [3. Memorando](#3-memo)
- [Apêndice](#appendix)
  - [API do Facebook Messenger](#facebook-messenger-api)
  - [Exemplos de mensagens da API do Facebook Messenger](#sample-facebook-messenger-api-messages)
    - [1. Text](#1-text)
    - [2. Audio](#2-audio)
    - [3. Localização](#3-location)
  - [Discussão](#discussion)
    - [Os detalhes essenciais da implementação de reconhecimento e escalabilidade de voz](#the-nitty-gritty-detail-of-implementing-voice-recognition-&-scalability)


#### Características:
- Reconhecimento de voz
- Entendendo comandos com Processamento de Linguagem Natural e acompanhamento contextual
- Pesquisa de negócios / restaurantes
- Pesquisa de Notícias em alta
- Speech-to-Text anotações (com acesso ao Cloud)
- Conversa de bate-papo

#### Screenshots:
![Optimist Prime Screenshots](https://monosnap.com/file/gCXyTugWB6IRdGScJBzHLuL9Vz9lMt.png)
**[Demo](https://www.facebook.com/optimistPrimeBot/)** (clique na mensagem para começar a conversar com o bot)


## Uso

> Nota: O Optimist Prime é implementado com APIs diferentes para recursos como gerenciamento de usuários, reconhecimento de voz, pesquisa em restaurantes, pesquisa de tendências de notícias, por isso leva algum tempo para configurar e colocar tudo em funcionamento. Para um "bot echo" mais básico que responda a você o que quer que você diga, use **`facebook-echobot.py`** ou vá para o aplicativo Messenger do Facebook [Início rápido](https://developers.facebook.com/docs/messenger-platform/quickstart/). O echo bot é útil para dar uma olhada rápida nas ideias fundamentais por trás de um Facebook Messenger Bot.

#### Dependências, banco de dados e chaves de API

Para construir seu próprio bot com todos os recursos do Optimist Prime, você precisará de alguns setups:

0. Instalar dependências: `pip install -r requirements.txt` (de preferência entrar em seu ambiente virtual `virtualenv`/`venv` -ler tudo sobre `pip` e `venv` [aqui](https://packaging.python.org/installing/))
1. [Crie uma página no Facebook](https://www.facebook.com/pages/create/): uma Página para "atribuir" ao Bot. O Bot será na verdade essa página, ou seja, você estará "falando" com a página
2. [Crie um aplicativo do Facebook](https://developers.facebook.com/docs/apps/register), obter seu token de acesso à página (detalhes no Facebook [Início rápido](https://developers.facebook.com/docs/messenger-platform/quickstart/))
3. Criar um banco de dados MongoDB (gerenciamento de usuários, gerenciamento de contexto de conversação, registro), um MongoDB local esta de bom tamanho ([Tutorial](https://scotch.io/tutorials/an-introduction-to-mongodb) para configurar uma instância local). Eu usei [mLab MongoDB] do Heroku (https://elements.heroku.com/addons/mongolab).Você levará 10 minutos para obter uma conta Heroku e criar um banco de dados MongoDB no [mLab](https://mlab.com/).

> É recomendado que a crição do banco de dados MongoDb seja realizada diretamente no [mLab](https://mlab.com/), pois isto irá evitar cadastro do seu cartão de crédito 
> Ao cadastrar o banco de dados deve-se cadastrar ao menos um usuário (Users) para uso posterior e anotar a conecção que será fornecida (Ex: mongodb://<dbuser>:<dbpassword>@ds263089.mlab.com:63089/webdev), substituindo posteriormente o <dbuser> e <dbpassword> pelas credenciais adequadas. O "webdev" no exemplo apresentado é o banco de dados que será requisitado nas configurações posteriormente. 

Então faça algumas configurações no `config.py`:

1. Credenciais do banco de dados MongoDB (criadas acima)
2. Chave da API do Yelp (recurso de Negócios / Pesquisa de Restaurante): [Pegue um aqui](https://www.yelp.com/developers/manage_api_keys) (Mais detalhes abaixo, já que o Yelp agora tem uma API v2 estável e uma visualização de desenvolvedor v3)
3. Nome de usuário e senha da API do Speech to Text do IBM Watson: [Pegue um aqui](https://console.ng.bluemix.net/) (Mais detalhes abaixo)
4. Simsimi: [Pegue um aqui](http://developer.simsimi.com/) (Chave experimental gratuita de 7 dias)
5. Defina sua própria configuração local: crie uma pasta chamada `instance` e crie outro arquivo `config.py` nela.([Mais sobre configurações do Flask](http://flask.pocoo.org/docs/0.11/config/))

Para executar localmente, tão simples quanto:
```bash
python facebookbot.py 3000
```
Ou com `gunicorn` (como é feito no Heroku) ([Flask e gunicorn tutorial](https://www.digitalocean.com/community/tutorials/how-to-serve-flask-applications-with-gunicorn-and-nginx-on-ubuntu-14-04))
```bash
gunicorn facebookbot:app -b localhost:3000
```

Agora que você tem o bot rodando, você precisa configurar um webhook para o Facebook para enviar mensagens que o bot recebe. Isto pode ser feito com o `ngrok`, que irá configurar um túnel seguro para o seu servidor localhost:
```bash
./ngrok http 3000
```
> O ngrok pode não funcionar se estiver rodando numa máquina virtual, tal como, VirtualBox, ou por restrições do proxy da sua rede.

![ngrok](https://monosnap.com/file/HJckHGSorOuoEqm6kBNFb7MQWdNeHf.png)

O endereço do webhook que será inserido no Facebook pode ser do ngrok ou do heroku, caso for utilizar diretamente no cloud do heroku, executando os comandos descritos abaixo do heroku: 

**Execute os comandos do Heroku abaixo para criar e fazer deploy da sua aplicação:**
```bash
# Faz Login
heroku login

# Cria uma App no Heroku
heroku create

# Adiciona alterações no repositório local do Git 
git add . 

# Salva as alterações e insere uma 'Mensagem' a sua escolha para que seja submetido ao servidor
git commit -m "Mensagem"

# Faz deploy da aplicação no servidor heroku
git push heroku master 

# Garante que a última versão da aplicação esta ativa
heroku ps:scale web=1

# Abre a aplicação na página Web
heroku open
```

Em iterações posteriores, tudo o que você precisa fazer com Heroku são as 3 linhas gloriosas:
```bash
git add .
git commit -am "Awesome commit"
git push heroku master
```
Obtenha o URL `https` (o Facebook exige webhooks `https`) e assine seu aplicativo do Facebook neste webhook. O token de verificação é o seu próprio token definido em `OWN_VERIFICATION_TOKEN` no `config.py`.

![webhook](https://monosnap.com/file/LJITuhaxURs7MXpDQrvDKBk7yIrBER.png)

##### Implantando na nuvem

Foi fornecido o Procfile para implantação no **Heroku**. Você pode criar um aplicativo Heroku, criar um dyno grátis e implantar seu próprio Optimist Prime com [este tutorial](https://devcenter.heroku.com/articles/getting-started-with-python#introduction).

Para que o reconhecimento de voz funcione, precisamos incluir `ffmpeg` em nosso Heroku dyno, o que poderia ser feito adicionando um Heroku Buildpack à guia Configurações do seu aplicativo no Dashboard:
`https://github.com/jonathanong/heroku-buildpack-ffmpeg-latest.git`
![buildpack](https://monosnap.com/file/KrXLU25L6NEWvP36lNO4GgCOLWF419.png)

Finalmente, defina sua variável de ambiente para o caminho para o `ffmpeg`:
```bash
heroku config:set FFMPEG_PATH=/app/vendor/ffmpeg/ffmpeg
```
Ou na guia de configurações do seu aplicativo no Painel:
![configvar](https://monosnap.com/file/eipdi9mPeKyQDTLvQWMcNUHEtJZ7lG.png)

Agora você está pronto para implantar. [Tutorial sobre como implantar com Heroku e git](https://devcenter.heroku.com/articles/git).

**Amazon Web Service**: Gostom muito da AWS e tive grande experiência com o Beanstalk. No entanto, se você quiser usar o AWS, precisará ir além da obtenção de um certificado SSL para ter um webhook seguro. Para os propósitos do Optimist Prime, eu decidi ir com o Heroku, já que ele fornece prontamente uma conexão `https`.

## Reconhecimento de voz
O Reconhecimento de Voz é implementado com as duas [API de Fala para Texto do IBM Watson] (https://www.ibm.com/watson/developercloud/speech-to-text.html) e [Google Cloud Speech API] (https: //cloud.google.com/speech/) (o padrão é o IBM Watson, pois o Google Cloud Speech ainda está em Beta e os testes demonstram que o Watson é mais preciso). A implementação atual é baseada em seus métodos RESTful (ambos suportam processamento em tempo real com WebSocket e WebRTC, respectivamente). Ambos estão disponíveis gratuitamente no uso em nível de desenvolvimento.

Para usar o Speech-to-Text do IBM Watson, você precisará criar uma [conta do IBM Bluemix](https://console.ng.bluemix.net/) e incluir o serviço em sua conta, recuperar o nome de usuário da API e senha. Por fim, copie essas credenciais para `Speech / credentials.py`.

![O Console do Bluemix](https://monosnap.com/file/Z20JjWmcyZCth9oSAIEyg0aZVB1JTr.png)

Para usar a Google Cloud Speech API, o processo é um pouco mais complicado, pois você precisará exportar as credenciais do Google como uma variável de ambiente. No entanto, todo o processo é bem documentado pelo Google aqui. Assim que você tiver o arquivo-chave da Conta de Serviço (json) e exportou a variável de ambiente `GOOGLE_APPLICATION_CREDENTIALS` para o local do arquivo-chave, você está pronto para continuar.

Para alternar entre o IBM Watson e o Google para reconhecimento de fala: Configurando a variável de ambiente da seguinte forma:
```bash
export FB_BOT_STT_API_PROVIDER=GOOGLE
export FB_BOT_STT_API_PROVIDER=IBM
```

O texto resultante processado por esta API Speech-to-Text é então retornado como uma mensagem de texto que o bot recebe, que então passa pela PNL para detectar comandos / conversações.

## Processamento de linguagem natural

Optimist Bot recebe comandos de usuários como entrada de texto e voz, e compreende comandos em linguagem natural.

Isto é feito usando a NLP [biblioteca] padrão (http://www.clips.ua.ac.be/pages/pattern-en), que permite ao bot desconstruir a entrada de texto do usuário e reconhecer partes do discurso . Por enquanto, o modelo para categorizar comandos é simples com palavras de parada e estruturas de sentença, mas à medida que nossos dados crescem, podemos começar a construir uma categorização mais complexa de aprendizado de máquina para cada função.

O sistema de comando permite que os usuários usem os seguintes recursos, todos sob a pasta `Utils`.

## Recursos personalizados

### 1. Pesquisa de negócios / restaurantes

Comandos de exemplo:
```
bar irlandês por perto.
encontrar restaurantes chineses.
Encontre-me uma boa cafeteria por aqui.
mostre-me comida chinesa por perto.
Encontre restaurantes mexicanos perto daqui.
Eu quero ter comida vietnamita hoje à noite.
há um churrasco coreano nas proximidades?
Quais são algumas churrasqueira do Camboja por perto?
encontrar um restaurante etíope.
Eu quero comida mediterrânea.
encontre um alvo.
Encontre-me um KFC por perto.
Eu gostaria de comer no McDonalds.
Encontre-me alguns lugares de fast food na cidade de ohio.
Encontre-me uma cervejaria perto do centro de San Francisco.
```

Depois de receber o comando, o Optimist Prime pedirá a sua localização. Você pode inserir um nome de local **baseado em texto / voz** ou enviar sua **localização exata de GPS** (com o Facebook Messenger em dispositivos móveis). A API de pesquisa do Yelp exige uma coordenada para pesquisa de local exata, portanto, a pesquisa inversa de nome-local para coordenada é tratada pelo recurso de geocodificação da biblioteca Geopy. Uma alternativa (provavelmente mais atualizada e mais inteligente com nomes complexos) seria [Google Maps Geocoding API] (https://developers.google.com/maps/documentation/geocoding/intro). O Optimist Prime atualmente usa o `Geopy`. O Optimist Prime também oferece salvar sua localização para referência futura.
![Pesquisa de localização inteligente](https://monosnap.com/file/5ox1ff0xx1l6r2cjTD7o7Gcb8aqgKF.png)

Optimist Prime aproveita a API do Yelp. Incluído no código está o APIv2 (estável) e o APIv3 (visualização do desenvolvedor). Ambos exigem que você adquira sua chave de API.

[Obter chave de API para v2](https://www.yelp.com/developers/manage_api_keys)

[Obter chave de API para v3](https://www.yelp.com/developers/v3/preview)

Depois que você tiver sua chave de API, coloque-a no `config.py`

Para alternar entre v2 e v3, altere a instrução `import` em` facebookbot.py` entre `yelp_search_v2` e` yelp_search_v3`

```python
from Utils.Yelp import yelp_search_v3 as yelp_search
```

### 2. Pesquisa de Notícias em alta

Comandos de exemplo:

```
me dê notícias sobre UniRitter.
encontrar notícias sobre chatbot.
me dê algumas notícias sobre as eleições presidenciais no Brasil.
Receba notícias de tendências sobre tecnologia de informação.
procure as últimas notícias sobre futebol.
```

![Pesquisa de Notíciash](https://monosnap.com/file/wTn8lqcV1mgryNs5bMEG2LFcCQb1ff.png)

A Trending News Search usa a [API Webhose.io] (https://webhose.io/SDK). O serviço rastreia a Web em busca de notícias junto com sua força social (curtidas no Facebook, compartilhamentos, postagens no Twitter). No caso de usuários que pesquisam tópicos não relacionados a tendências ou nichos, o Optimist Prime reduz seus critérios de "tendências", bem como o tempo de pesquisa, para obter os melhores resultados.

### 3. Memorando

Comandos de exemplo:

```
memorize isso para mim: [continue falando seu memorando]
memorize isso: [continue falando seu memorando]
memorize isso (pare de falar, o Optimist Prime pedirá para você iniciar seu memorando)
você pode memorizar isso para mim?
```

![Memorando](https://monosnap.com/file/cYHCLLXhdSTPeQi0qtTl3dhF7S209k.png)

Esse recurso ainda está em seus conceitos iniciais. Depois que o usuário salvar um memorando, ele pode acessá-lo na web com o link fornecido pelo bot.

A infeliz notícia é que o Facebook usa user_ids diferentes para o Facebook Profile (que é usado para login) e Messenger. Uma mesma conta teria 2 user_ids diferentes, e o bot receberia apenas o user_id do Messenger da API do Messenger, impossibilitando a implementação de um recurso de login do Facebook seguro. A solução atual é permitir que os usuários acessem seu próprio memorando dentro do chat do bot usando user_ids como caminhos de URL para consulta. No futuro pode-se usar o link de conta para isso.

## Licença
* Licença MIT, veja `LICENSE.txt`

## Versão 
* Versão 1.0

## APÊNDICE

#### API do Facebook Messenger
https://developers.facebook.com/docs/messenger-platform/product-overview


#### Exemplos de mensagens da API do Facebook Messenger

##### 1. Texto
```json
{
    "object": "page",
    "entry": [
        {
            "id": "1384358948246110",
            "time": 1473197313689,
            "messaging": [
                {
                    "sender": {
                        "id": "1389166911110336"
                    },
                    "recipient": {
                        "id": "1384358948246110"
                    },
                    "timestamp": 1473197313651,
                    "message": {
                        "mid": "mid.1473197313635:0a67934dfc4f04a629",
                        "seq": 7651,
                        "text": "Hey"
                    }
                }
            ]
        }
    ]
}
```

##### 2. Audio
```json
{
    "object": "page",
    "entry": [
        {
            "id": "1384358948246110",
            "time": 1473197300200,
            "messaging": [
                {
                    "sender": {
                        "id": "1389166911110336"
                    },
                    "recipient": {
                        "id": "1384358948246110"
                    },
                    "timestamp": 1473197300143,
                    "message": {
                        "mid": "mid.1473197298861:d6cf1fae1ad44ff234",
                        "seq": 7650,
                        "attachments": [
                            {
                                "type": "audio",
                                "payload": {
                                    "url": "https://cdn.fbsbx.com/v/t59.3654-21/14109832_10209906561878191_940661414_n.mp4/audioclip-1473197298000-2056.mp4?oh=85e027f68e17fa0b1c189c3d7f3164bf&oe=57D0B0F3"
                                }
                            }
                        ]
                    }
                }
            ]
        }
    ]
}
```

##### 3. Localização
```json
{
    "object": "page",
    "entry": [
        {
            "id": "1384358948246110",
            "time": 1473197244135,
            "messaging": [
                {
                    "sender": {
                        "id": "1389166911110336"
                    },
                    "recipient": {
                        "id": "1384358948246110"
                    },
                    "timestamp": 1473197244008,
                    "message": {
                        "mid": "mid.1473197243814:3803076c5438a13036",
                        "seq": 7646,
                        "attachments": [
                            {
                                "title": "Hung's Location",
                                "url": "https://www.facebook.com/l.php?u=https%3A%2F%2Fwww.bing.com%2Fmaps%2Fdefault.aspx%3Fv%3D2%26pc%3DFACEBK%26mid%3D8100%26where1%3D40.070706608101%252C%2B-82.525680894134%26FORM%3DFBKPL1%26mkt%3Den-US&h=mAQE9bbu3&s=1&enc=AZPC_QlKfUFl7dehzlPuSpsio7LMKtRwyM58oaqUtt89CfKBofXVoW48cYrASUdCm-MYSpFMI2ejgmTR90taFN4wyv0aCYNH_GG3MR5sEe62NQ",
                                "type": "location",
                                "payload": {
                                    "coordinates": {
                                        "lat": 40.070706608101,
                                        "long": -82.525680894134
                                    }
                                }
                            }
                        ]
                    }
                }
            ]
        }
    ]
}
```

Existem também outros tipos úteis de mensagem (também implementados neste bot), incluindo Resposta Rápida, Postback na [documentação da API do Facebook Messenger] (https://developers.facebook.com/docs/messenger-platform/webhook-reference/message-received).


## Discussão

#### Os detalhes essenciais da implementação de reconhecimento e escalabilidade de voz

A captura para o processamento de mensagens de voz da API do Facebook Messenger é **convertendo o mp3 compactado do Facebook em um formato de entrada válido** para a API Speech-to-Text. Tanto a IBM quanto o Google não suportam mp3, e seu formato de entrada inclui os principais formatos de áudio como WAV, FLAC, OGG, etc. Portanto, o Optimist Prime precisa baixar o áudio mp3, convertê-lo para WAV e carregá-lo na Speech API, que é uma viagem de ida e volta que aumenta significativamente o tempo de resposta para cada comando de áudio. Neste projeto, foi utilizado o `ffmpeg` que foi chamado como um `subprocesso` do Python para converter o áudio.

> `subprocess` é uma ferramenta Python que permite disparar comandos parecidos com linhas de comando, então o que o programa faz é equivalente a ele chamar outro programa "digitando este comando na linha de comando"

![ffmpeg no subprocesso](https://monosnap.com/file/LWCiJmkZsTRcgeEBXRr5xGBU4gzIpi.png)

Sob o capô, o bot faz o seguinte:
- Recebe um json do comando de áudio do usuário
- Faz o download deste arquivo de áudio
- Usa o `ffmpeg` para converter:
+ Usa Python `subprocess` para iniciar um comando ffmpeg nativo (assim como seria feito no shell de comando)
+ Coloca a saída de áudio convertida em um pipe como um arquivo blob
+ Devolve este arquivo blob
- Carrega o arquivo blob de áudio convertido para a Speech API

Essa abordagem pega a saída do `ffmpeg` diretamente do pipe e faz o upload sem salvá-lo em um arquivo temporário e depois faz o upload do arquivo. 

Isso levanta questões de escalabilidade (em teoria): várias conversões simultâneas podem maximizar a memória, já que isso é feito no canal. No entanto, acredito que este não seria o gargalo em escala, como a maioria dos arquivos de áudio tendem a ser inferior a 1MB, então para vários usuários, o gargalo estaria na conexão para baixar / carregar arquivos, em vez da memória. para converter todos esses arquivos. Os arquivos serão feitos com a conversão antes que outro arquivo seja baixado. Esta hipótese tem que ser testada.

Quando um usuário envia um áudio para o bot, o bot "receberá" uma URL para o arquivo, conforme processado no código abaixo no arquivo bot principal `facebookbot.py`:
[Código para processar diferentes tipos de mensagens recebidas](https://monosnap.com/file/rsb20Cxn5WUKFZ7hDLhjHBagMbk0rF.png)
