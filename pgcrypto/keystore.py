class KeyStore:
    public_key = None
    private_key = None
    default_key_retrieval_function = None

    @staticmethod
    def set_keys(public_key, private_key):
        KeyStore.public_key = public_key
        KeyStore.private_key = private_key

    @staticmethod
    def reset_keys():
        KeyStore.public_key = None
        KeyStore.private_key = None

    @staticmethod
    def get_public_key():
        if KeyStore.public_key:
            return KeyStore.public_key
        if KeyStore.default_key_retrieval_function:
            return KeyStore.default_key_retrieval_function()[0]
        raise ValueError('No public key set')

    @staticmethod
    def get_private_key():
        if KeyStore.private_key:
            return KeyStore.private_key
        if KeyStore.default_key_retrieval_function:
            return KeyStore.default_key_retrieval_function()[1]
        raise ValueError('No private key set')


@contextmanager
def key_provider(public_key:str, private_key:str):
    KeyStore.set_keys(public_key, private_key)
    try:
        yield None
    except InternalError as e:
        if len(e.args) >= 1 and e.args[0].strip() == "Wrong key":
            raise InternalError('Wrong private or public key was given.')
        raise e
    finally:
        KeyStore.reset_keys()
