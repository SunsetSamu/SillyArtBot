
async def conditions(self, ctx, tema: str):
    guild_id = str(ctx.guild.id)
    data = self.bot.guild_data[guild_id]

    # 0 0 0
    # 0 0 1
    # 0 1 0
    # 0 1 1
    # 1 0 0
    # 1 0 1
    # 1 1 0
    # 1 1 1

    if data.get('last_announcement_id') is None and data.get('current_challenge', {}).get('next_theme') is None and tema is None:
        # si no hay un reto activo y no hay una tematica para el siguiente y el input no contiene una tematica
        # 0 0 0
        await self.bot.announce_weekly_challenge(guild_id, data)
        await ctx.send(f"✅ Un nuevo reto ha sido iniciado (forzado) con la temática: **{data['current_challenge']['theme']}**")

    elif data.get('last_announcement_id') is None and data.get('current_challenge', {}).get('next_theme') is None and tema is not None:
        # si no hay un reto activo y no hay una tematica para el siguiente y el input contiene una tematica
        # 0 0 1
        data['current_challenge']['next_theme'] = tema
        self.bot.save_data()
        await self.bot.announce_weekly_challenge(guild_id, data)
        await ctx.send(f"✅ Un nuevo reto ha sido iniciado (forzado) con la temática: **{data['current_challenge']['theme']}**")

    elif data.get('last_announcement_id') is None and data.get('current_challenge', {}).get('next_theme') is not None and tema is None:
        # si no hay un reto activo y hay una tematica para el siguiente y el input no contiene una tematica
        # 0 1 0
        await self.bot.announce_weekly_challenge(guild_id, data)
        await ctx.send(f"✅ Un nuevo reto ha sido iniciado (forzado) con la temática: **{data['current_challenge']['theme']}**")

    elif data.get('last_announcement_id') is None and data.get('current_challenge', {}).get('next_theme') is not None and tema is not None:
        # si no hay un reto activo y hay una tematica para el siguiente y el input contiene una tematica
        # 0 1 1
        await self.bot.announce_weekly_challenge(guild_id, data)
        data['current_challenge']['next_theme'] = tema
        self.bot.save_data()
        await ctx.send(f"✅ Un nuevo reto ha sido iniciado (forzado) con la tematica programada: **{data['current_challenge']['theme']}**\n⚠️✅ Se ha configurado una nueva tematica para el siguiente reto.")

    elif data.get('last_announcement_id') is not None and data.get('current_challenge', {}).get('next_theme') is None and tema is None:
        # si hay un reto activo pero no hay una tematica para el siguiente y el input no contiene una tematica
        # 1 0 0
        await ctx.send("⚠️❌ **No permitido: ya hay un reto activo.**\n⚠️ Si quieres empezar un reto nuevo sin importarte la tematica primero termina el anterior *(puedes usar* `[]endchallenge` *y ya luego* `[]startchallenge` *)*\n⚠️ Si tu intencion es programar la tematica del proximo reto usa `[]startchallenge + siguiente tematica`") 
    
    elif data.get('last_announcement_id') is not None and data.get('current_challenge', {}).get('next_theme') is None and tema is not None:
        # si hay un reto activo pero no hay una tematica para el siguiente y el input contiene una tematica
        # 1 0 1
        data['current_challenge']['next_theme'] = tema
        self.bot.save_data()
        await ctx.send("⚠️✅ Ya hay un reto activo. La temática se guardará para el siguiente reto.")
                       
    elif data.get('last_announcement_id') is not None and data.get('current_challenge', {}).get('next_theme') is not None and tema is None:
        # si hay un reto activo y hay una tematica para el siguiente y el input no contiene una tematica
        # 1 1 0
        await ctx.send("⚠️❌ **No permitido: ya hay un reto activo.**\n⚠️ Si quieres empezar un reto nuevo con la siguiente tematica entonces termina el anterior *(puedes usar* `[]endchallenge` *y ya luego* `[]startchallenge` *)*\n⚠️ Si tu intencion es programar una nueva tematica del proximo reto usa `[]startchallenge + siguiente tematica` (esto reemplazará la temática programada actualmente)")

    elif data.get('last_announcement_id') is not None and data.get('current_challenge', {}).get('next_theme') is not None and tema is not None:
        # si hay un reto activo y hay una tematica para el siguiente y el input contiene una tematica
        # 1 1 1
        data['current_challenge']['next_theme'] = tema
        self.bot.save_data()
        await ctx.send("⚠️❌ **No permitido: ya hay un reto activo.**\n⚠️✅Se ha reemplazado la temática anterior.")
    
    else:
        await ctx.send("⚠️❌ **ERROR: DESCONOCIDO... WTF**")
        pass

                    
                    

 
