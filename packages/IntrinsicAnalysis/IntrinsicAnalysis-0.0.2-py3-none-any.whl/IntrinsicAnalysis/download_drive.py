from google_drive_downloader import GoogleDriveDownloader as gdd


files_ids = [
    ('armenian-armtdp-ud-2.5-191206.udpipe', '1IQCpQuT9S-7pwYvKQDRmAR9Xt94Cd9A8'),

    ('resources.json', '1oM5g2dMAc3R78hqBl58BTVgm9FNRRspe'),
    ('hy/depparse/armtdp.pt', '1BD6QEQ3NdyTLdr4iJZX2RHjCrKiQ26by'),
    ('hy/lemma/armtdp.pt', '1RlaQaWpdcMtWHIY3ir1pwztElxmTEoVj'),
    ('hy/mwt/armtdp.pt', '1F5IKNXIttkn-UFMR-v7yo0He0taY3GH7'),
    ('hy/pos/armtdp.pt', '180ZFLCTodvJ7RtiQdiK-xC70aVO0PV2O'),
    ('hy/pretrain/armtdp.pt', '1q5crp4Fw8zhW7ogVB3jZfgKSwUy222FL'),
    ('hy/tokenize/armtdp.pt', '1TBMPbpAmZMrMzU1uCprk6Z-OykzXm2By')
]

for name, id in files_ids:
    gdd.download_file_from_google_drive(file_id=id,
                                        dest_path='/tmp/intrinsic_analysis/essential_models/' + name,
                                        showsize=True)
