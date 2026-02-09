import os
import discord
from discord.ext import commands
import asyncio
import time
start_time = time.time()


# Ambil token dari environment variable
token = os.getenv("DISCORD_TOKEN")

# Cek apakah token berhasil diambil
if not token:
    raise RuntimeError("DISCORD_TOKEN belum diset di Railway Variables")
    exit()  # Keluar jika token tidak ditemukan


# Konfigurasi bot
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.presences = True

async def safe_delete(ctx):
    try:
        await ctx.message.delete()
    except:
        pass



async def safe_delete(ctx):
    try:
        await ctx.message.delete()
    except:
        pass

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Bot {bot.user.name} sudah online cuy!')
    print(f'Bot ID: {bot.user.id}')
    print('-' * 50)

@bot.command(name='ping')
async def ping(ctx):
    """Command untuk cek apakah bot aktif"""
    await ctx.message.delete()  # Hapus pesan user
    latency = round(bot.latency * 1000)  # Konversi ke milidetik
    await ctx.send(f'🏓 Pong! `{latency}ms` - Bot sedang aktif ✓')

@bot.command(name='hello')
async def hello(ctx):
    """Command untuk menyapa bot"""
    await ctx.send(f'Halo {ctx.author.name}! Saya adalah bot Discord pertamamu! 👋')

@bot.command(name='bantuan')
async def bantuan_command(ctx):
    """Menampilkan daftar command"""
    await ctx.message.delete()  # Hapus pesan user
    help_text = """
    **📚 Daftar Command Bot:**

    `ping` - Cek apakah bot aktif
    `hello` - Bot akan menyapa kamu
    `bantuan` - Menampilkan pesan ini 😪 
    `clear [max 100]` - untuk menghapus pesan 
    `userinfo` - info profil
    `say` - agar bot mengatakan apa yg lu tulis
    `serverinfo` - mengetahui server ini
    `uptime` - waktu bot berjalan

    """
    await ctx.send(help_text)




@bot.command(name='clear')
async def clear_messages(ctx, amount: int = 5):
    """Command untuk menghapus pesan di channel"""
    await ctx.message.delete()  # Hapus pesan user

    # Cek apakah user punya izin
    if not ctx.author.guild_permissions.manage_messages:
        await ctx.send('❌ Kamu tidak punya izin untuk menggunakan command ini!')
        return
    
    # Validasi jumlah
    if amount < 1:
        await ctx.send('❌ Jumlah pesan minimal 1!')
        return
    
    if amount > 100:
        await ctx.send('❌ Maksimal hapus 100 pesan sekaligus!')
        return
    
    try:
        # Hapus pesan
        deleted = await ctx.channel.purge(limit=amount+1)
        
        # Kirim konfirmasi
        await ctx.send(f'🗑️ **{len(deleted)}** pesan telah dihapus!', delete_after=3)
        
        # Log di console
        print(f'{ctx.author.name} menghapus {len(deleted)} pesan di #{ctx.channel.name}')
        
    except Exception as e:
        await ctx.send(f'❌ Error: {str(e)}')


@bot.command(name='userinfo')
async def userinfo(ctx):
    """Menampilkan informasi tentang user"""
    await ctx.message.delete()  # Hapus pesan user
    
    # Ambil user yang mengirim command
    user = ctx.author
    
    # Karena kita sudah di dalam server, ctx.author adalah Member object
    # Ambil data yang dibutuhkan
    user_name = user.name
    user_discriminator = user.discriminator
    user_id = user.id
    avatar_url = user.display_avatar.url
    
    # Format tanggal
    created_date = user.created_at.strftime('%d %B %Y')
    account_days = (discord.utils.utcnow() - user.created_at).days
    
    joined_date = user.joined_at.strftime('%d %B %Y')
    joined_days = (discord.utils.utcnow() - user.joined_at).days
    
    # Ambil roles
    roles_list = []
    for role in user.roles:
        if role.name != "@everyone":
            roles_list.append(role.mention)
    roles_str = ", ".join(roles_list) if roles_list else "Tidak ada roles"
    roles_count = len(roles_list)
    
    # Status
    status_map = {
        discord.Status.online: "🟢 ONLINE",
        discord.Status.idle: "🟡 IDLE",
        discord.Status.dnd: "🔴 DND",
        discord.Status.offline: "⚫ OFFLINE"
    }
    status_str = status_map.get(user.status, "⚫ UNKNOWN")
    
    # Buat embed
    embed = discord.Embed(
        title=f"👤 Informasi User: {user_name}",
        color=discord.Color.blue(),
        timestamp=discord.utils.utcnow()
    )
    
    embed.set_thumbnail(url=avatar_url)
    
    embed.add_field(name="📛 Nama", value=f"**{user_name}**", inline=True)
    embed.add_field(name="#️⃣ Tag", value=f"**#{user_discriminator}**", inline=True)
    embed.add_field(name="🆔 ID", value=f"**{user_id}**", inline=False)
    
    embed.add_field(name="📅 Akun Dibuat", value=f"**{created_date}**\n({account_days} hari lalu)", inline=True)
    embed.add_field(name="📅 Gabung Server", value=f"**{joined_date}**\n({joined_days} hari lalu)", inline=True)
    embed.add_field(name="🤖 Bot?", value="✅ Ya" if user.bot else "❌ Tidak", inline=True)
    
    embed.add_field(name="🎭 Roles", value=f"**{roles_count}** roles\n{roles_str}", inline=False)
    embed.add_field(name="🌐 Status", value=status_str, inline=True)
    
    await ctx.send(embed=embed, delete_after=30)


@bot.command(name="uptime")
async def uptime(ctx):
    """ini untuk melihat seberapa lama bot menyala"""
    await ctx.message.delete() # menghapus pesan user
    up = int(time.time() - start_time)
    h = up // 3600
    m = (up % 3600) // 60
    s = up % 60
    await ctx.send(f"⏱️ Uptime: **{h}j {m}m {s}d**")

@bot.command(name="serverinfo")
async def serverinfo(ctx):
    """info keseluruhan server"""
    await ctx.message.delete() # menghapus pesan user
    g = ctx.guild
    # Mengambil informasi owner
    owner_name = g.owner.name if g.owner else "Tidak diketahui"
    await ctx.send(
        f"🏠 **{g.name}**\n"
        f"👥 Members: **{g.member_count}**\n"
        f"📅 Dibuat: **{g.created_at.strftime('%d %B %Y')}**"
        f"👑 Owner: {owner_name}"
    )

@bot.command(name="say")
@commands.has_permissions(manage_messages=True)
async def say(ctx, *, text: str):
    """perintah untuk bot mengulangi perkataan"""
    try:
        await ctx.message.delete()
    except:
        pass
    await ctx.send(text)
@say.error
async def say_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("❌ Kamu gak punya izin.")


@bot.command(name="avatar")
async def avatar(ctx, member: discord.Member = None):
    """
    Ambil avatar user.
    Pakai:
    -avatar
    -avatar @user
    """
    try:
        await ctx.message.delete()
    except:
        pass

    member = member or ctx.author
    avatar_url = member.display_avatar.url  # aman untuk avatar server/global

    embed = discord.Embed(
        title=f"🖼️ Avatar: {member}",
        color=discord.Color.blue()
    )
    embed.set_image(url=avatar_url)
    embed.set_footer(text=f"Diminta oleh: {ctx.author.display_name}")

    await ctx.send(embed=embed)
    


# Ganti TOKEN_DISINI dengan token bot kamu
bot.run(token)    # gunakan token dari emvironment variable