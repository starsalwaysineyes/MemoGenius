import openai

filename=""
ifile=open("/www/wwwroot/mg.dawnaurora.top/test/input.txt",'r')
filename=ifile.read()
ifile.close()


openai.api_key = "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"
#"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"

audio_file= open("/www/wwwroot/mg.dawnaurora.top/uploads/"+filename, "rb")

transcript = openai.Audio.transcribe("whisper-1", audio_file)

#print(transcript['text'])


cont="会议内容如下："+transcript['text']

completion = openai.ChatCompletion.create(
  model="gpt-3.5-turbo",
  messages=[
    {"role": "system", "content": "你是我的会议记录助手，你需要把会议中的内容都用中文进行要点总结，要能覆盖所有有意义的点。要求越详细越好，和数据有关的信息需全部记录。"},
    {"role": "user", "content": cont}
  ]
)

f=open("/www/wwwroot/mg.dawnaurora.top/test/result.txt",'w')
s=str(completion.choices[0].message["content"])#.decode("unicode-escape")
#print(s)
f.write(s)
f.close()





