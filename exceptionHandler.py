import sys
async def InteractionException(e, interaction):
    """Controla las excepciones causadas con una interacción

    Args:
        e (Excepcion): Excepción a ser mostrada
        interaction (interaction): Interacción que causó la excepción
    """
    exception_type, exception_object, exception_traceback = sys.exc_info()
    line_number = exception_traceback.tb_lineno
    filename = exception_traceback.tb_frame.f_code.co_filename
    excp = interaction.author.name + " causó: _'" + str(e) + "'_, revisa las entradas de datos"
    print(excp + " in " + filename + " in line: " + str(line_number))
    await interaction.respond(excp)
