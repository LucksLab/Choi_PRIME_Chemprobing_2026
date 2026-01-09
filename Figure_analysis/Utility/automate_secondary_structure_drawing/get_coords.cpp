extern "C"
{
#include <ViennaRNA/fold.h>
#include <ViennaRNA/fold_compound.h>
#include <ViennaRNA/utils.h>
#include <ViennaRNA/params.h>
#include <ViennaRNA/plotting/RNApuzzler/RNApuzzler.h>
}

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

/**
 * @brief Extract coordinates from RNA structure and output as CSV.
 *
 * Usage:
 *     ./get_coords <sequence> <dot-bracket-structure> [output_file.csv]
 *
 * Writes a CSV with columns: nt,x,y,arc
 */
int main(int argc, char *argv[])
{
    // Silent exit if no arguments provided
    if (argc == 1)
    {
        return 0;
    }

    if (argc < 3)
    {
        fprintf(stderr, "Usage: %s <sequence> <dot-bracket-structure> [output_file.csv]\n", argv[0]);
        return 1;
    }

    const char *sequence = argv[1];
    const char *structure = argv[2];
    const char *output_file = (argc >= 4) ? argv[3] : "coordinates.csv";

    if (strlen(sequence) != strlen(structure))
    {
        fprintf(stderr, "Error: Sequence and structure must be of the same length.\n");
        return 1;
    }

    float *x = NULL, *y = NULL;
    double *arcs = NULL;

    if (!vrna_plot_coords_puzzler(structure, &x, &y, &arcs, NULL))
    {
        fprintf(stderr, "Error: vrna_plot_coords_puzzler failed.\n");
        return 1;
    }

    FILE *fp = fopen(output_file, "w");
    if (!fp)
    {
        perror("Failed to open file for writing");
        free(x);
        free(y);
        free(arcs);
        return 1;
    }

    fprintf(fp, "nt,x,y,arc\n");
    for (int i = 0; i < (int)strlen(structure); i++)
    {
        fprintf(fp, "%c,%f,%f,%f\n", sequence[i], x[i], y[i], arcs[i]);
    }

    fclose(fp);
    free(x);
    free(y);
    free(arcs);

    return 0;
}