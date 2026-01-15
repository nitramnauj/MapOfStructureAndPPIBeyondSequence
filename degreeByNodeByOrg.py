import pandas as pd

organism = 'human'

# Leer los archivos CSV
degree_df = pd.read_csv('degreeByNode_'+organism+'.csv')
biogrid_df = pd.read_csv('biogrid_by_uniprot.csv')

print(f"Items en degreeByNode.csv: {len(degree_df)}")
print(f"Items en biogrid_by_uniprot.csv: {len(biogrid_df)}")

# Hacer un merge basado en la columna "Uniprot"
# Esto automáticamente omitirá los registros donde Uniprot no esté en ambos archivos
merged_df = pd.merge(degree_df, biogrid_df, on='Uniprot', how='inner')

print(f"Items after merge: {len(merged_df)}")

# Ordenar por la columna "Grado" en orden descendente
merged_df = merged_df.sort_values("Grado",ascending=False)
merged_df = merged_df.reset_index(drop=True)

output_file = 'degreeByNode_with_biogrid_'+organism+'.csv'
merged_df.to_csv(output_file, index=False)

print(f"\nFile saved as: {output_file}")
print(merged_df.head())

# Mostrar estadísticas del merge
print(f"Max Degree: {merged_df['Grado'].max()}")
print(f"Min Degree: {merged_df['Grado'].min()}")
print(f"Ave Degree: {merged_df['Grado'].mean():.2f}")

uniprot_no_encontrados = len(degree_df) - len(merged_df)
if uniprot_no_encontrados > 0:
    print(f"\nWarning: {uniprot_no_encontrados} items from degreeByNode.csv were skiped because its Uniprot was not in biogrid_by_uniprot.csv")
